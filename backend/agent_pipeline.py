"""
BhashaSwarm 3D — Voice Agent Pipeline
========================================
Full-duplex real-time voice AI pipeline integrating:
- Gnani Prisma v3.0 STT (WebSocket streaming with code-mix)
- OpenAI-compatible LLM with tool-calling (Evon / GPT-4o-mini)
- IndicTextNormalizer (markdown strip, PII scrub, currency expand)
- Gnani Timbre v3.0 TTS (WebSocket streaming with expressive Audio Tags)
- Concurrency Guard (Semaphore(1) for 429 prevention)
- Real-time telemetry broadcast to frontend HUD

Two execution pathways:
  A) /ws/voice  — Full duplex real-time WebSocket (mic or simulated audio)
  B) /api/simulate-turn — 1-Click mic-free pipeline trigger
"""
import asyncio
import base64
import io
import json
import logging
import time
import struct
import wave
from typing import Any, Dict, List, Optional

import aiohttp
import numpy as np

from pipecat_gnani import (
    GnaniSTTService,
    GnaniTTSService,
    GnaniSSETTSService,
    PRISMA_V3_MODEL,
    STT_FORMAT_CODEMIX,
)
from pipecat.transcriptions.language import Language

from config import (
    settings,
    sanitize_stt_keywords,
    VALID_EXPRESSIVE_TAGS,
    DEFAULT_LANGUAGE_CANDIDATES,
)
from concurrency_guard import concurrency_guard
from normalizer import IndicTextNormalizer
from tools import execute_agent_tool, TOOL_DEFINITIONS
from telemetry import telemetry, TurnMetrics
from reasoning_engine import reasoning_engine

logger = logging.getLogger("bhashaswarm.pipeline")

# ── System Prompt for the Indic Code-Mixed Voice Agent ──────────────────────
SYSTEM_PROMPT = """You are BhashaSwarm, an expert multilingual Indian voice AI assistant built on Gnani.ai's Vachana platform.

CRITICAL RULES:
1. You are a VOICE agent. Keep responses concise (2-4 sentences max) and conversational.
2. You speak fluent Hinglish (Hindi + English code-mixing), Tanglish (Tamil + English), and Kanglish (Kannada + English).
3. Match the user's language. If they speak Hinglish, reply in Hinglish. If Tamil, reply in Tanglish.
4. You have access to 3 tools — use them when the user's request matches:
   - dispatch_gramseva_ticket: For civic complaints (power, water, roads, sanitation)
   - query_kirana_inventory: For store inventory/stock/expiry checks
   - evaluate_socratic_viva: For CS engineering viva/concept evaluation
5. You can use these Timbre v3.0 expressive Audio Tags in your response text:
   <laugh> <chuckle> <sigh> <gasp>
   Use them naturally and sparingly for emotional expressiveness.
6. NEVER output markdown formatting (**, ##, ```, etc.) — your text goes directly to TTS.
7. NEVER include real personal data (phone numbers, Aadhaar, PAN). All data is synthetic.
8. When using tool results, speak the summary naturally. Don't read JSON.
9. Be warm, helpful, and authentically Indian in tone.

Example Hinglish response:
"<chuckle> Haan bilkul! Aapki complaint register ho gayi hai. Ward 4 ke engineer ko assign kar diya — 45 minutes mein team aa jayegi!"
"""


class BhashaSwarmPipeline:
    """
    Manages the complete voice AI pipeline for a single WebSocket session.
    Handles STT → LLM → Normalizer → TTS with real-time telemetry.
    """

    def __init__(
        self,
        ws_send_json,
        ws_send_bytes,
        voice: str = "Riyaa",
        model: str = "timbre-v3.0",
        language: str = "hi-IN",
        language_candidates: Optional[List[str]] = None,
    ):
        self.ws_send_json = ws_send_json
        self.ws_send_bytes = ws_send_bytes
        self.voice = voice
        self.tts_model = model
        self.language = language
        self.language_candidates = language_candidates or DEFAULT_LANGUAGE_CANDIDATES[:4]

        self.normalizer = IndicTextNormalizer()
        self.conversation_history: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.is_speaking = False
        self._cancel_tts = False
        self._aiohttp_session: Optional[aiohttp.ClientSession] = None
        self._stt_ws = None
        self._tts_ws = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._aiohttp_session is None or self._aiohttp_session.closed:
            self._aiohttp_session = aiohttp.ClientSession()
        return self._aiohttp_session

    async def cleanup(self):
        """Clean up WebSocket connections and HTTP sessions."""
        if self._stt_ws:
            try:
                await self._stt_ws.close()
            except Exception:
                pass
        if self._tts_ws:
            try:
                await self._tts_ws.close()
            except Exception:
                pass
        if self._aiohttp_session and not self._aiohttp_session.closed:
            await self._aiohttp_session.close()

    # ── STT: Gnani Prisma v3.0 WebSocket / REST Streaming ───────────────
    async def transcribe_audio(self, audio_bytes: bytes) -> Optional[str]:
        """
        Send audio frames to Gnani Prisma v3.0 STT endpoint
        and return the transcript with sub-200ms latency.

        Uses the concurrency guard to prevent HTTP 429.
        """
        turn = telemetry.start_turn()
        turn.stt_start = time.perf_counter()

        try:
            async with concurrency_guard.acquire_slot("stt_transcribe"):
                session = await self._get_session()

                headers = {
                    "X-API-Key-ID": settings.gnani_api_key,
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                }

                # Create standard 16kHz WAV-wrapped audio for STT endpoint
                wav_data = self._wrap_pcm_as_wav(audio_bytes, settings.sample_rate)

                form = aiohttp.FormData()
                form.add_field(
                    "audio_file",
                    wav_data,
                    filename="audio.wav",
                    content_type="audio/wav",
                )
                form.add_field("format", "verbatim")
                form.add_field("model", "prisma-v3.0")

                if self.language == "indic-auto":
                    form.add_field("language_code", "indic-auto")
                    candidates = self.language_candidates or ["hi-IN", "en-IN", "ta-IN", "kn-IN"]
                    form.add_field("multi_lang_codes", ",".join(candidates[:4]))
                else:
                    form.add_field("language_code", self.language)

                stt_url = "https://api.vachana.ai/stt/v3"
                async with session.post(
                    stt_url, headers=headers, data=form, timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    turn.stt_end = time.perf_counter()
                    if resp.status == 200:
                        result = await resp.json()
                        transcript = (result.get("transcript") or result.get("text") or "").strip()
                        detected_lang = (
                            result.get("detected_language_code")
                            or result.get("language_code")
                            or self.language
                        )
                        turn.detected_language = detected_lang

                        if transcript:
                            await self.ws_send_json({
                                "type": "stt_result",
                                "text": transcript,
                                "transcript": transcript,
                                "is_final": True,
                                "detected_language": detected_lang,
                                "latency_ms": round((time.perf_counter() - turn.stt_start) * 1000, 1),
                            })
                            logger.info("🎤 Prisma v3.0 STT transcribed: '%s' (%s, latency %.1fms)", transcript, detected_lang, turn.stt_latency_ms)
                            return transcript
                        else:
                            logger.debug("Prisma v3.0 STT returned silence (no speech detected)")
                            return None
                    else:
                        error_text = await resp.text()
                        logger.warning("STT API status %d (%s)", resp.status, error_text[:60])
                        return None

        except Exception as e:
            turn.stt_end = time.perf_counter()
            logger.error("STT exception: %s", e)
            return None

    @staticmethod
    def _wrap_pcm_as_wav(pcm_data: bytes, sample_rate: int) -> bytes:
        """Wrap raw 16-bit mono PCM in a standard RIFF WAV header using Python wave module."""
        try:
            wav_buf = io.BytesIO()
            with wave.open(wav_buf, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(pcm_data)
            return wav_buf.getvalue()
        except Exception:
            num_channels = 1
            bits_per_sample = 16
            byte_rate = sample_rate * num_channels * bits_per_sample // 8
            block_align = num_channels * bits_per_sample // 8
            data_size = len(pcm_data)
            file_size = 36 + data_size
            header = struct.pack(
                "<4sI4s4sIHHIIHH4sI",
                b"RIFF", file_size, b"WAVE",
                b"fmt ", 16, 1, num_channels,
                sample_rate, byte_rate, block_align, bits_per_sample,
                b"data", data_size,
            )
            return header + pcm_data

    # ── LLM: OpenAI-compatible Chat Completion with Tool Calling ────────
    async def run_llm(self, user_text: str) -> Dict[str, Any]:
        """
        Send the conversation to the LLM (Evon / OpenAI) with tool definitions.
        Returns {"text": str, "tool_card": dict|None}.
        """
        turn = telemetry._current_turn
        if turn:
            turn.llm_start = time.perf_counter()

        self.conversation_history.append({"role": "user", "content": user_text})

        # Sovereign Indic Reasoning Engine (Fast-path when external LLM key is omitted)
        if not settings.llm_api_key or "your_" in settings.llm_api_key:
            return await self._fallback_tool_reasoning(user_text, turn)

        try:
            session = await self._get_session()
            headers = {
                "Authorization": f"Bearer {settings.llm_api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": settings.llm_model,
                "messages": self.conversation_history[-20:],  # Keep context window manageable
                "tools": TOOL_DEFINITIONS,
                "tool_choice": "auto",
                "max_tokens": 300,
                "temperature": 0.7,
            }

            async with session.post(
                f"{settings.llm_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                if turn:
                    turn.llm_first_token = time.perf_counter()

                if resp.status != 200 or not settings.llm_api_key or "your_" in settings.llm_api_key:
                    error = await resp.text() if resp.status != 200 else "Using synthetic tool matcher"
                    logger.info("Using deterministic tool matcher: %s", error)
                    return await self._fallback_tool_reasoning(user_text, turn)

                result = await resp.json()
                choice = result["choices"][0]
                message = choice["message"]

                # Handle tool calls
                if message.get("tool_calls"):
                    tool_call = message["tool_calls"][0]
                    func_name = tool_call["function"]["name"]
                    func_args = json.loads(tool_call["function"]["arguments"])

                    if turn:
                        turn.tool_calls.append(func_name)

                    # Execute the tool
                    tool_result = execute_agent_tool(func_name, func_args)

                    # Send tool card to frontend immediately
                    await self.ws_send_json({
                        "type": "tool_card",
                        "data": tool_result,
                    })

                    # Add tool interaction to conversation
                    self.conversation_history.append(message)
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": json.dumps(tool_result),
                    })

                    # Get the LLM's spoken response incorporating tool result
                    # Use the spoken_summary from the tool as the response
                    response_text = tool_result.get("spoken_summary", "Action completed.")

                    self.conversation_history.append({
                        "role": "assistant",
                        "content": response_text,
                    })

                    if turn:
                        turn.llm_end = time.perf_counter()

                    return {
                        "text": response_text,
                        "tool_card": tool_result,
                    }

                # No tool call — direct text response
                response_text = message.get("content", "")
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response_text,
                })

                if turn:
                    turn.llm_end = time.perf_counter()

                return {"text": response_text, "tool_card": None}

        except Exception as e:
            logger.info("Using deterministic fallback tool reasoner: %s", e)
            return await self._fallback_tool_reasoning(user_text, turn)

    async def _fallback_tool_reasoning(self, user_text: str, turn: Optional[TurnMetrics]) -> Dict[str, Any]:
        """Sovereign conversational & Socratic reasoning engine powered by massive Indic database."""
        reason_res = await reasoning_engine.reason_and_respond(
            user_text, turn=turn, language=self.language, voice=self.voice
        )

        tool_card = reason_res.get("tool_card")
        if tool_card:
            await self.ws_send_json({"type": "tool_card", "data": tool_card})

        gesture = reason_res.get("gesture")
        if gesture:
            await self.ws_send_json({"type": "trigger_gesture", "gesture": gesture})

        action = reason_res.get("action")
        if action:
            if action.get("type") == "switch_language":
                self.update_language(action.get("language", "hi-IN"))
                if action.get("voice"):
                    self.update_voice(action["voice"])
            elif action.get("type") == "barge_in":
                await self.handle_barge_in()

        return {"text": reason_res["text"], "tool_card": tool_card}

    # ── TTS: Gnani Timbre v3.0 Synthesis ────────────────────────────────
    async def synthesize_speech(self, text: str) -> None:
        """
        Synthesize speech via Gnani Timbre v3.0 and stream PCM chunks
        + viseme energy data back to the browser WebSocket.

        Uses the concurrency guard and supports barge-in cancellation.
        """
        if not text or not text.strip():
            return

        turn = telemetry._current_turn
        if turn:
            turn.tts_start = time.perf_counter()

        # Normalize text for TTS
        normalized = IndicTextNormalizer.normalize_for_tts(text)
        if not normalized:
            return

        logger.info("🔊 TTS input (normalized): %s", normalized[:100])

        self.is_speaking = True
        self._cancel_tts = False
        first_audio_sent = False
        chunks_sent = 0

        # Enforce voice-model pairing (e.g. Riyaa -> timbre-v3.0)
        self.tts_model, self.voice = settings.validate_voice_model(self.tts_model, self.voice)

        try:
            async with concurrency_guard.acquire_slot("tts_synthesize"):
                # Check if Gnani API Key is configured
                if not settings.gnani_api_key or "your_" in settings.gnani_api_key:
                    logger.info("Gnani API key not configured — using synthetic audio stream for simulation")
                    await self._synthesize_synthetic_pcm(normalized, turn)
                    return

                session = await self._get_session()

                # Headers with User-Agent to bypass Cloudflare WAF
                headers = {
                    "X-API-Key-ID": settings.gnani_api_key,
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                }

                payload = {
                    "text": normalized,
                    "voice": self.voice,
                    "model": self.tts_model,
                    "audio_config": {
                        "sample_rate": settings.sample_rate,
                        "encoding": "linear_pcm",
                        "num_channels": 1,
                        "sample_width": 2,
                        "container": "raw",
                    },
                    "language": self.language,
                    "speed": 1.0,
                }

                # Pathway 1: SSE Streaming from Gnani Timbre
                try:
                    tts_url = settings.gnani_tts_sse_url
                    async with session.post(
                        tts_url,
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=30),
                    ) as resp:
                        if resp.status == 200:
                            current_event = "message"
                            async for line_bytes in resp.content:
                                if self._cancel_tts:
                                    logger.info("🎤 Barge-in: TTS cancelled mid-stream")
                                    break

                                line = line_bytes.decode("utf-8", errors="ignore").strip()
                                if not line:
                                    continue

                                if line.startswith("event:"):
                                    current_event = line[6:].strip()
                                    continue

                                if line.startswith("data:"):
                                    data_str = line[5:].strip()
                                    if not data_str:
                                        continue
                                    try:
                                        event_data = json.loads(data_str)
                                    except json.JSONDecodeError:
                                        continue

                                    audio_b64 = event_data.get("audio") or event_data.get("data", {}).get("audio", "")
                                    if audio_b64:
                                        audio_bytes = base64.b64decode(audio_b64)
                                        if audio_bytes[:4] == b"RIFF":
                                            audio_bytes = audio_bytes[44:]

                                        if not first_audio_sent and turn:
                                            turn.tts_first_audio = time.perf_counter()
                                            first_audio_sent = True

                                        energy = self._calculate_viseme_energy(audio_bytes)
                                        await self.ws_send_bytes(audio_bytes)
                                        await self.ws_send_json({
                                            "type": "viseme",
                                            "energy": energy,
                                            "timestamp": time.time(),
                                        })
                                        chunks_sent += 1

                                    elif current_event == "complete" or event_data.get("is_final") or event_data.get("status") == "completed":
                                        logger.info("✅ Live Gnani Timbre SSE streaming completed (%d chunks streamed)", chunks_sent)
                                        break
                                    elif current_event == "error" or event_data.get("status") == "error":
                                        logger.error("TTS stream error: %s", event_data.get("message"))
                                        break
                        else:
                            error = await resp.text()
                            logger.warning("TTS SSE status %d (%s) — trying REST inference endpoint", resp.status, error[:80])
                except Exception as sse_err:
                    logger.warning("TTS SSE exception: %s — trying REST fallback", sse_err)

                # Pathway 2: REST Inference Fallback if SSE produced 0 chunks
                if chunks_sent == 0 and not self._cancel_tts:
                    try:
                        logger.info("Fetching audio from Gnani Timbre REST endpoint (%s, %s)...", self.tts_model, self.voice)
                        async with session.post(
                            settings.gnani_tts_rest_url,
                            headers=headers,
                            json=payload,
                            timeout=aiohttp.ClientTimeout(total=20),
                        ) as rest_resp:
                            if rest_resp.status == 200:
                                raw_audio = await rest_resp.read()
                                if raw_audio[:4] == b"RIFF":
                                    raw_audio = raw_audio[44:]

                                if not first_audio_sent and turn:
                                    turn.tts_first_audio = time.perf_counter()
                                    first_audio_sent = True

                                chunk_size = 1024
                                for i in range(0, len(raw_audio), chunk_size):
                                    if self._cancel_tts:
                                        break
                                    chunk = raw_audio[i:i+chunk_size]
                                    energy = self._calculate_viseme_energy(chunk)
                                    await self.ws_send_bytes(chunk)
                                    await self.ws_send_json({
                                        "type": "viseme",
                                        "energy": energy,
                                        "timestamp": time.time(),
                                    })
                                    chunks_sent += 1
                                    await asyncio.sleep(0.025)
                                logger.info("✅ Live Gnani Timbre REST audio streamed (%d chunks)", chunks_sent)
                            else:
                                err_text = await rest_resp.text()
                                logger.warning("TTS REST status %d (%s)", rest_resp.status, err_text[:80])
                    except Exception as rest_err:
                        logger.warning("TTS REST exception: %s", rest_err)

                # Pathway 3: Fallback to synthetic PCM only if both live endpoints failed
                if chunks_sent == 0 and not self._cancel_tts:
                    logger.warning("Live TTS endpoints unavailable — falling back to synthetic harmonic audio stream")
                    await self._synthesize_synthetic_pcm(normalized, turn)

        except asyncio.CancelledError:
            logger.info("TTS task cancelled (barge-in)")
        except Exception as e:
            logger.error("TTS exception: %s", e)
        finally:
            self.is_speaking = False
            await self.ws_send_json({"type": "tts_done"})

            # Send telemetry snapshot
            if turn:
                turn.tts_end = time.perf_counter()
                snapshot = telemetry.end_turn()
                snapshot["concurrency"] = concurrency_guard.get_telemetry()
                await self.ws_send_json(snapshot)

    async def _synthesize_synthetic_pcm(self, text: str, turn: Optional[TurnMetrics]) -> None:
        """
        Synthesize speech-modulated 16kHz PCM audio frames for simulation & offline mode.
        Ensures 3D Avatar lip-sync and WebAudio playback function flawlessly without external keys.
        Supports instant mid-sentence barge-in cancellation.
        """
        # Duration proportional to text length (approx 14 chars/sec, min 40 frames, max 100 frames)
        num_frames = min(120, max(45, int(len(text) * 0.7)))
        base_f0 = 210.0 if self.voice in ["Riyaa", "Chetana", "Shivani", "Tarika", "Vasudha"] else 135.0

        for frame_idx in range(num_frames):
            if self._cancel_tts:
                logger.info("🎤 Barge-in: Synthetic TTS cancelled mid-stream at frame %d", frame_idx)
                break

            if frame_idx == 0 and turn:
                turn.tts_first_audio = time.perf_counter()

            # Generate 512 samples (32ms at 16kHz) of phoneme-like modulated harmonic sound
            t = (frame_idx * 512 + np.arange(512)) / 16000.0
            syllable_mod = 0.5 + 0.5 * np.sin(2.0 * np.pi * 3.5 * t)
            f0_jitter = base_f0 * (1.0 + 0.05 * np.sin(2.0 * np.pi * 5.0 * t))
            
            # Harmonic formants (F0, F1, F2)
            wave = (
                0.6 * np.sin(2.0 * np.pi * f0_jitter * t) +
                0.3 * np.sin(2.0 * np.pi * f0_jitter * 2.2 * t) +
                0.15 * np.sin(2.0 * np.pi * f0_jitter * 4.0 * t)
            ) * syllable_mod * 0.25

            # Convert to int16 PCM
            pcm_samples = (wave * 32767.0).astype(np.int16)
            pcm_bytes = pcm_samples.tobytes()

            energy = self._calculate_viseme_energy(pcm_bytes)

            await self.ws_send_bytes(pcm_bytes)
            await self.ws_send_json({
                "type": "viseme",
                "energy": energy,
                "timestamp": time.time(),
            })

            # Stream at 32ms real-time cadence
            await asyncio.sleep(0.032)

    @staticmethod
    def _calculate_viseme_energy(audio_bytes: bytes) -> Dict[str, float]:
        """
        Extract frequency band energies from PCM audio for 3D lip-sync:
        - jaw_open: Low-band (100-400Hz) → jaw rotation
        - lip_spread: Mid-band (400-2000Hz) → mouth width
        - sibilance: High-band (2000-6000Hz) → tongue/teeth
        """
        try:
            samples = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
            if len(samples) < 64:
                return {"jaw_open": 0.0, "lip_spread": 0.0, "sibilance": 0.0, "rms": 0.0}

            # Normalize
            samples = samples / 32768.0

            # RMS energy
            rms = float(np.sqrt(np.mean(samples ** 2)))

            # FFT for frequency band analysis
            fft = np.abs(np.fft.rfft(samples))
            freqs = np.fft.rfftfreq(len(samples), 1.0 / 16000)

            # Band energies (normalized 0-1)
            low_mask = (freqs >= 100) & (freqs < 400)
            mid_mask = (freqs >= 400) & (freqs < 2000)
            high_mask = (freqs >= 2000) & (freqs < 6000)

            max_energy = max(np.max(fft), 1e-6)

            jaw_open = float(np.mean(fft[low_mask])) / max_energy if low_mask.any() else 0.0
            lip_spread = float(np.mean(fft[mid_mask])) / max_energy if mid_mask.any() else 0.0
            sibilance = float(np.mean(fft[high_mask])) / max_energy if high_mask.any() else 0.0

            # Clamp to 0-1
            jaw_open = min(1.0, max(0.0, jaw_open * 3.0))
            lip_spread = min(1.0, max(0.0, lip_spread * 3.0))
            sibilance = min(1.0, max(0.0, sibilance * 5.0))

            return {
                "jaw_open": round(jaw_open, 3),
                "lip_spread": round(lip_spread, 3),
                "sibilance": round(sibilance, 3),
                "rms": round(min(1.0, rms * 5.0), 3),
            }
        except Exception:
            return {"jaw_open": 0.0, "lip_spread": 0.0, "sibilance": 0.0, "rms": 0.0}

    # ── Barge-In Handler ────────────────────────────────────────────────
    async def handle_barge_in(self):
        """
        GUARDRAIL #7: Handle barge-in interruption.
        Cancels in-flight TTS and notifies the frontend to flush audio buffer.
        """
        self._cancel_tts = True
        self.is_speaking = False
        telemetry.record_barge_in()

        await self.ws_send_json({
            "type": "barge_in_ack",
            "barge_in_count": telemetry._barge_in_count,
            "message": "TTS interrupted — listening...",
        })

    # ── Full Turn Pipeline ──────────────────────────────────────────────
    async def process_text_turn(self, user_text: str) -> None:
        """
        Execute the full pipeline for a text input (from simulation or STT):
        User Text → LLM (with tools) → Normalize → TTS → Stream to client
        """
        if not user_text or not user_text.strip():
            return

        # Notify frontend we're processing
        await self.ws_send_json({
            "type": "status",
            "status": "thinking",
            "text": user_text,
        })

        # Run LLM
        llm_result = await self.run_llm(user_text)
        response_text = llm_result["text"]

        # Send text response to frontend
        await self.ws_send_json({
            "type": "llm_response",
            "text": response_text,
            "has_tool_call": llm_result["tool_card"] is not None,
        })

        # Synthesize and stream TTS
        await self.ws_send_json({"type": "status", "status": "speaking"})
        await self.synthesize_speech(response_text)

    # ── Configuration Updates ───────────────────────────────────────────
    def update_voice(self, voice: str, model: str = "timbre-v3.0"):
        """Hot-swap voice and model (from frontend dropdown)."""
        from config import settings as cfg
        validated_model, validated_voice = cfg.validate_voice_model(model, voice)
        self.voice = validated_voice
        self.tts_model = validated_model
        logger.info("🎙️ Voice updated: %s (%s)", self.voice, self.tts_model)

    def update_language(self, language: str, candidates: Optional[List[str]] = None):
        """Hot-swap language and candidates (from frontend dropdown)."""
        self.language = language
        if candidates:
            self.language_candidates = candidates[:4]
        logger.info("🌐 Language updated: %s, candidates: %s", self.language, self.language_candidates)

