"""
BhashaSwarm 3D — FastAPI Server
=================================
Two execution pathways:

  Pathway A: /ws/voice — Full-duplex real-time WebSocket
    Receives 16kHz 16-bit mono PCM from browser mic, streams through
    Gnani Prisma v3.0 STT → LLM → IndicTextNormalizer → Gnani Timbre v3.0 TTS,
    streams back binary PCM + JSON telemetry.

  Pathway B: /api/simulate-turn — 1-Click mic-free pipeline trigger
    Accepts a preset Hinglish/Tanglish utterance, runs the live LLM + TTS pipeline,
    streams results over the active WebSocket.

Also serves:
  GET  /api/health — Health check
  GET  /api/config — Frontend configuration (voices, languages)
  POST /api/simulate-turn — Simulation endpoint
"""
import asyncio
import json
import logging
import time
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config import (
    settings,
    TIMBRE_V30_VOICES,
    TIMBRE_V25_VOICES,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE_CANDIDATES,
)
from concurrency_guard import concurrency_guard
from agent_pipeline import BhashaSwarmPipeline
from telemetry import telemetry
from massive_db import db

# ── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-28s | %(levelname)-5s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("gnani.server")

# ── FastAPI App ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="Gnani Vachana 3D",
    description="Real-time Code-Mixed Indic Voice AI with 3D Avatar Lip-Sync",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Simulation Presets ──────────────────────────────────────────────────────
SIMULATION_PRESETS = {
    "hinglish_civic": {
        "id": "hinglish_civic",
        "label": "🇮🇳 Hinglish Civic Triage",
        "text": "Bhaiya Ward 4 MP Nagar mein raat se transformer spark kar raha hai, voltage fluctuate ho raha hai, urgent ticket raise karo!",
        "language": "hi-IN",
    },
    "hinglish_kirana": {
        "id": "hinglish_kirana",
        "label": "🛒 Hinglish Kirana Copilot",
        "text": "Check karo Amul Taaza batch ka stock kitna bacha hai aur expiry kab hai? Loss bachane ke liye kya karein?",
        "language": "hi-IN",
    },
    "hinglish_viva": {
        "id": "hinglish_viva",
        "label": "🎓 Hinglish Socratic Viva",
        "text": "Sir Operating System mein Deadlock aur Starvation ka main difference yeh hai ki deadlock mein processes infinite wait karte hain — mera concept check kijiye.",
        "language": "hi-IN",
    },
    "tanglish_switch": {
        "id": "tanglish_switch",
        "label": "🎭 Tanglish Language Switch",
        "text": "Vanakkam! Can you switch to Tamil-English code-mixing and explain how Prisma v3.0 handles regional accents?",
        "language": "ta-IN",
    },
    "hinglish_banking": {
        "id": "hinglish_banking",
        "label": "💳 UPI & Banking Dispute",
        "text": "SBI account se UPI payment 5000 rupaye deduct ho gaya lekin merchant ko credit nahi hua, U19 error aa raha hai, dispute raise karo!",
        "language": "hi-IN",
    },
    "hinglish_health": {
        "id": "hinglish_health",
        "label": "💊 Jan Aushadhi Health Triage",
        "text": "Doctor ne Dolo 650 aur Pantocid 40 likha hai, Jan Aushadhi generic alternative kitne ka padega aur kitni bachat hogi?",
        "language": "hi-IN",
    },
    "hinglish_railway": {
        "id": "hinglish_railway",
        "label": "🚆 RailMadad 139 Triage",
        "text": "Train 20607 Vande Bharat Express ke coach C3 mein AC bilkul cooling nahi kar raha hai, RailMadad complaint dispatch kijiye!",
        "language": "hi-IN",
    },
    "hinglish_agri": {
        "id": "hinglish_agri",
        "label": "🌾 Kisan Crop Disease Advisory",
        "text": "Basmati Dhaan ki fasal mein patte par brown spots ban rahe hain aur blast rog lag raha hai, kaunsa keetnashak spray karein?",
        "language": "hi-IN",
    },
    "armour365_scam": {
        "id": "armour365_scam",
        "label": "🛡️ Scam Defense (armour365™)",
        "text": "Mujhe ek call aaya hai bol rahe hain CBI Cyber Crime se bol rahe hain, mere naam pe FedEx narcotics parcel nikla hai aur mera Digital Arrest ho gaya hai, turant paise transfer karne bol rahe hain!",
        "language": "hi-IN",
    },
    "kannada_main": {
        "id": "kannada_main",
        "label": "🇮🇳 Kannada (Main Character)",
        "text": "Namaskara! Kannada dalli mathadi. Gnani Vachana 3D Yeshwanthpur APMC mandi rate mathu kisan sahayaka bagge vivarisi.",
        "language": "kn-IN",
    },
}


class SimulationRequest(BaseModel):
    preset_id: Optional[str] = None
    custom_text: Optional[str] = None
    language: Optional[str] = "hi-IN"


class ChatRequest(BaseModel):
    text: str
    language: Optional[str] = "hi-IN"
    voice: Optional[str] = "Riyaa"


class SettingsUpdateRequest(BaseModel):
    gnani_api_key: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_model: Optional[str] = None
    default_tts_voice: Optional[str] = None
    default_language: Optional[str] = None


# ── Global State ────────────────────────────────────────────────────────────
active_pipelines: dict[str, BhashaSwarmPipeline] = {}


# ── REST Endpoints ──────────────────────────────────────────────────────────
@app.get("/api/health")
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "Gnani Vachana 3D",
        "gnani_api_configured": bool(settings.gnani_api_key),
        "llm_configured": bool(settings.llm_api_key),
        "concurrency": concurrency_guard.get_telemetry(),
        "database": db.get_stats(),
    }


@app.get("/api/db/stats")
async def get_db_stats():
    """Return live metrics on the 10,000+ record Massive Indic Database."""
    return db.get_stats()


@app.get("/api/db/search")
async def search_db(q: str = "", limit: int = 20):
    """Instant <1ms multi-domain search across 10,000+ FMCG, Civic Ward, Mandi, and Viva records."""
    if not q or not q.strip():
        return {"query": "", "count": 0, "results": []}
    matches = db.search_all(q.strip(), limit=limit)
    return {
        "query": q,
        "count": len(matches),
        "results": matches,
    }


@app.get("/api/db/sample")
async def get_db_sample(domain: str = "all"):
    """Get sample records for interactive UI explorer."""
    samples = {
        "products": db.products[:5],
        "wards": db.wards[:5],
        "mandi": db.mandi_rates[:5],
        "viva": db.socratic_bank[:5],
        "banking": db.banking_records[:5],
        "health": db.healthcare_records[:5],
        "railway": db.railway_records[:5],
        "agritech": db.agritech_records[:5],
    }
    if domain in samples:
        return {domain: samples[domain]}
    return samples


@app.get("/api/config")
async def get_config():
    return {
        "voices": {
            "timbre-v3.0": TIMBRE_V30_VOICES,
            "timbre-v2.5": TIMBRE_V25_VOICES,
        },
        "languages": SUPPORTED_LANGUAGES,
        "default_voice": settings.default_tts_voice,
        "default_model": settings.default_tts_model,
        "default_language": settings.default_language,
        "language_candidates": DEFAULT_LANGUAGE_CANDIDATES,
        "presets": list(SIMULATION_PRESETS.values()),
        "sample_rate": settings.sample_rate,
    }


@app.post("/api/settings")
async def update_settings_endpoint(req: SettingsUpdateRequest):
    """Update API credentials at runtime from the settings drawer."""
    if req.gnani_api_key is not None:
        settings.gnani_api_key = req.gnani_api_key.strip()
    if req.llm_api_key is not None:
        settings.llm_api_key = req.llm_api_key.strip()
    if req.llm_model is not None:
        settings.llm_model = req.llm_model.strip()
    if req.default_tts_voice is not None:
        settings.default_tts_voice = req.default_tts_voice.strip()
    if req.default_language is not None:
        settings.default_language = req.default_language.strip()

    is_gnani_ok = bool(settings.gnani_api_key and "your_" not in settings.gnani_api_key)
    is_llm_ok = bool(settings.llm_api_key and "your_" not in settings.llm_api_key)

    logger.info("⚙️ Runtime settings updated — Gnani configured: %s, LLM configured: %s", is_gnani_ok, is_llm_ok)
    return {
        "status": "updated",
        "gnani_api_configured": is_gnani_ok,
        "llm_configured": is_llm_ok,
    }


@app.post("/api/simulate-turn")
async def simulate_turn(req: SimulationRequest):
    """
    GUARDRAIL #8: 1-Click Mic-Free Pipeline Trigger.
    Injects a preset utterance into the active pipeline so judges can test
    without a microphone.
    """
    # Get the text to process
    if req.preset_id and req.preset_id in SIMULATION_PRESETS:
        preset = SIMULATION_PRESETS[req.preset_id]
        text = preset["text"]
        language = preset.get("language", "hi-IN")
    elif req.custom_text:
        text = req.custom_text
        language = req.language or "hi-IN"
    else:
        return JSONResponse(
            status_code=400,
            content={"error": "Provide preset_id or custom_text"},
        )

    # Find an active pipeline to inject into
    if active_pipelines:
        pipeline_id = next(iter(active_pipelines))
        pipeline = active_pipelines[pipeline_id]
        pipeline.update_language(language)

        # Run the turn asynchronously
        asyncio.create_task(pipeline.process_text_turn(text))

        return {
            "status": "triggered",
            "text": text,
            "language": language,
            "pipeline_id": pipeline_id,
        }
    else:
        # Fallback: standalone pipeline execution
        captured_data = []
        async def dummy_json(data):
            captured_data.append(data)
        async def dummy_bytes(data):
            pass
        pipeline = BhashaSwarmPipeline(dummy_json, dummy_bytes)
        pipeline.update_language(language)
        asyncio.create_task(pipeline.process_text_turn(text))
        return {
            "status": "triggered",
            "text": text,
            "language": language,
            "pipeline_id": "standalone",
        }


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """
    Direct REST endpoint for text interaction with Evon v3.3 reasoning.
    """
    text = req.text.strip()
    if not text:
        return JSONResponse(status_code=400, content={"error": "Text cannot be empty"})

    if active_pipelines:
        pipeline_id = next(iter(active_pipelines))
        pipeline = active_pipelines[pipeline_id]
        if req.language:
            pipeline.update_language(req.language)
        if req.voice:
            pipeline.update_voice(req.voice)
        asyncio.create_task(pipeline.process_text_turn(text))
        return {
            "status": "processing",
            "text": text,
            "pipeline_id": pipeline_id,
        }
    else:
        captured_reply = []
        async def capture_json(data):
            if data.get("type") == "llm_response":
                captured_reply.append(data.get("text", ""))
        async def dummy_bytes(data):
            pass
        pipeline = BhashaSwarmPipeline(capture_json, dummy_bytes, voice=req.voice or "Riyaa")
        pipeline.update_language(req.language or "hi-IN")
        await pipeline.process_text_turn(text)
        reply = " ".join(captured_reply) if captured_reply else "Turn processed."
        return {
            "status": "completed",
            "text": text,
            "reply": reply,
            "pipeline_id": "standalone"
        }


# ── WebSocket Voice Endpoint ───────────────────────────────────────────────
@app.websocket("/ws/voice")
async def voice_websocket(ws: WebSocket):
    """
    Pathway A: Full-duplex real-time WebSocket for voice AI.

    Protocol:
      Client → Server:
        - Binary frames: 16kHz 16-bit mono PCM audio (1024 bytes per frame)
        - JSON: {"type": "barge_in"} to interrupt TTS
        - JSON: {"type": "config", "voice": "...", "language": "..."} to update settings
        - JSON: {"type": "simulate", "preset_id": "..."} to trigger simulation
        - JSON: {"type": "text_input", "text": "..."} for typed text input

      Server → Client:
        - Binary frames: 16kHz 16-bit mono PCM TTS audio chunks
        - JSON: {"type": "stt_result", ...} interim/final transcripts
        - JSON: {"type": "llm_response", ...} LLM text response
        - JSON: {"type": "tool_card", ...} tool execution result card
        - JSON: {"type": "viseme", ...} lip-sync energy data
        - JSON: {"type": "telemetry", ...} latency metrics
        - JSON: {"type": "status", ...} pipeline state changes
        - JSON: {"type": "tts_done"} TTS synthesis complete
        - JSON: {"type": "barge_in_ack", ...} barge-in acknowledged
    """
    await ws.accept()
    pipeline_id = f"ws_{id(ws)}_{int(time.time())}"
    logger.info("🌐 WebSocket connected: %s", pipeline_id)

    # Helpers for sending data
    async def send_json(data: dict):
        try:
            await ws.send_json(data)
        except Exception:
            pass

    async def send_bytes(data: bytes):
        try:
            await ws.send_bytes(data)
        except Exception:
            pass

    # Create pipeline for this session
    pipeline = BhashaSwarmPipeline(
        ws_send_json=send_json,
        ws_send_bytes=send_bytes,
        voice=settings.default_tts_voice,
        model=settings.default_tts_model,
        language=settings.default_language,
    )
    active_pipelines[pipeline_id] = pipeline

    # Send connection confirmation
    await send_json({
        "type": "connected",
        "pipeline_id": pipeline_id,
        "config": {
            "voice": pipeline.voice,
            "model": pipeline.tts_model,
            "language": pipeline.language,
            "sample_rate": settings.sample_rate,
        },
        "concurrency": concurrency_guard.get_telemetry(),
    })

    # Audio buffer for accumulating mic frames
    audio_buffer = bytearray()
    silence_frames = 0
    speech_started = False
    noise_floor = 250.0
    SILENCE_FRAMES_CUTOFF = 14  # ~450ms of silence after speech to commit turn

    try:
        while True:
            message = await ws.receive()

            if message["type"] == "websocket.disconnect":
                break

            elif message["type"] == "websocket.receive":
                # Binary frame: audio data
                if "bytes" in message and message["bytes"]:
                    audio_data = message["bytes"]
                    audio_buffer.extend(audio_data)

                    # Dynamic Adaptive VAD: track noise floor & voice activity
                    import numpy as np
                    try:
                        samples = np.frombuffer(audio_data, dtype=np.int16)
                        rms = float(np.sqrt(np.mean(samples.astype(np.float32) ** 2)))
                        noise_floor = min(noise_floor * 0.99 + rms * 0.01, 1000.0)
                        threshold = max(350.0, noise_floor * 1.5)

                        if rms < threshold:
                            silence_frames += 1
                        else:
                            silence_frames = 0
                            speech_started = True

                        # Send interim waveform energy to frontend
                        await send_json({
                            "type": "mic_energy",
                            "rms": round(float(rms) / 32768.0, 4),
                        })

                    except Exception:
                        silence_frames += 1

                    # If speech was detected and silence followed, process the turn
                    if (
                        speech_started
                        and len(audio_buffer) > settings.pcm_frame_size * 6
                        and silence_frames >= SILENCE_FRAMES_CUTOFF
                    ):
                        audio_bytes = bytes(audio_buffer)
                        audio_buffer.clear()
                        silence_frames = 0
                        speech_started = False

                        # Process the audio turn via Gnani Prisma v3 STT
                        transcript = await pipeline.transcribe_audio(audio_bytes)
                        if transcript and transcript.strip():
                            await pipeline.process_text_turn(transcript)

                # Text frame: JSON commands
                elif "text" in message and message["text"]:
                    try:
                        data = json.loads(message["text"])
                    except json.JSONDecodeError:
                        continue

                    msg_type = data.get("type", "")

                    if msg_type == "barge_in":
                        await pipeline.handle_barge_in()
                        audio_buffer.clear()
                        speech_started = False
                        silence_frames = 0

                    elif msg_type == "mic_end":
                        # User stopped mic — process any buffered speech immediately
                        if len(audio_buffer) > settings.pcm_frame_size * 3:
                            audio_bytes = bytes(audio_buffer)
                            audio_buffer.clear()
                            silence_frames = 0
                            speech_started = False
                            transcript = await pipeline.transcribe_audio(audio_bytes)
                            if transcript and transcript.strip():
                                await pipeline.process_text_turn(transcript)

                    elif msg_type == "config":
                        if "voice" in data:
                            model = data.get("model", pipeline.tts_model)
                            pipeline.update_voice(data["voice"], model)
                        if "language" in data:
                            candidates = data.get("candidates")
                            pipeline.update_language(data["language"], candidates)
                        await send_json({
                            "type": "config_ack",
                            "voice": pipeline.voice,
                            "model": pipeline.tts_model,
                            "language": pipeline.language,
                        })

                    elif msg_type == "simulate":
                        preset_id = data.get("preset_id", "hinglish_civic")
                        if preset_id in SIMULATION_PRESETS:
                            preset = SIMULATION_PRESETS[preset_id]
                            pipeline.update_language(preset.get("language", "hi-IN"))
                            await pipeline.process_text_turn(preset["text"])

                    elif msg_type == "ping":
                        await send_json({"type": "pong", "timestamp": time.time()})

                    elif msg_type == "text_input":
                        text = data.get("text", "").strip()
                        if text:
                            await pipeline.process_text_turn(text)

    except WebSocketDisconnect:
        logger.info("🔌 WebSocket disconnected: %s", pipeline_id)
    except Exception as e:
        logger.error("WebSocket error: %s", e)
    finally:
        await pipeline.cleanup()
        active_pipelines.pop(pipeline_id, None)
        logger.info("🧹 Pipeline cleaned up: %s", pipeline_id)


import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app.mount("/", StaticFiles(directory=ROOT_DIR, html=True), name="static")

# ── Entry Point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    logger.info("🚀 Starting BhashaSwarm 3D Backend on port %d", settings.backend_port)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.backend_port,
        reload=False,
        log_level="info",
    )

