"""
BhashaSwarm 3D — Telemetry Tracker
====================================
Tracks real-time latency metrics for the live Cyber Telemetry HUD:
- STT latency (Prisma v3.0)
- LLM TTFT (Evon / OpenAI)
- TTS TTFA (Timbre v3.0)
- Detected language codes
- Barge-in interruptions
- 429 collision prevention count
"""
import time
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

logger = logging.getLogger("bhashaswarm.telemetry")


@dataclass
class TurnMetrics:
    """Metrics for a single conversational turn."""
    turn_id: int = 0
    stt_start: float = 0.0
    stt_end: float = 0.0
    llm_start: float = 0.0
    llm_first_token: float = 0.0
    llm_end: float = 0.0
    tts_start: float = 0.0
    tts_first_audio: float = 0.0
    tts_end: float = 0.0
    detected_language: str = ""
    tool_calls: List[str] = field(default_factory=list)

    @property
    def stt_latency_ms(self) -> float:
        if self.stt_start and self.stt_end:
            return round((self.stt_end - self.stt_start) * 1000, 1)
        return 0.0

    @property
    def llm_ttft_ms(self) -> float:
        if self.llm_start and self.llm_first_token:
            return round((self.llm_first_token - self.llm_start) * 1000, 1)
        return 0.0

    @property
    def tts_ttfa_ms(self) -> float:
        if self.tts_start and self.tts_first_audio:
            return round((self.tts_first_audio - self.tts_start) * 1000, 1)
        return 0.0

    @property
    def total_latency_ms(self) -> float:
        if self.stt_start and self.tts_first_audio:
            return round((self.tts_first_audio - self.stt_start) * 1000, 1)
        return 0.0


class TelemetryTracker:
    """
    Aggregates per-turn metrics and global counters for the live HUD.
    Thread-safe for single-event-loop async usage.
    """

    def __init__(self):
        self._turn_counter: int = 0
        self._current_turn: Optional[TurnMetrics] = None
        self._barge_in_count: int = 0
        self._total_turns: int = 0
        self._last_metrics: Dict[str, Any] = {}
        self._language_history: List[str] = []

    def start_turn(self) -> TurnMetrics:
        """Begin tracking a new conversational turn."""
        self._turn_counter += 1
        self._current_turn = TurnMetrics(turn_id=self._turn_counter)
        return self._current_turn

    def end_turn(self) -> Dict[str, Any]:
        """Finalize the current turn and cache the metrics snapshot."""
        self._total_turns += 1
        if self._current_turn:
            if self._current_turn.detected_language:
                self._language_history.append(self._current_turn.detected_language)
                # Keep last 20 language detections
                self._language_history = self._language_history[-20:]

            self._last_metrics = self.get_snapshot()
        return self._last_metrics

    def record_barge_in(self):
        """Increment the barge-in interruption counter."""
        self._barge_in_count += 1
        logger.info("🎤 Barge-in #%d recorded", self._barge_in_count)

    def get_snapshot(self) -> Dict[str, Any]:
        """
        Returns a telemetry snapshot suitable for WebSocket JSON broadcast
        to the CyberTelemetryHUD frontend component.
        """
        turn = self._current_turn
        return {
            "type": "telemetry",
            "turn_id": turn.turn_id if turn else 0,
            "stt_latency_ms": turn.stt_latency_ms if turn else 0.0,
            "llm_ttft_ms": turn.llm_ttft_ms if turn else 0.0,
            "tts_ttfa_ms": turn.tts_ttfa_ms if turn else 0.0,
            "total_latency_ms": turn.total_latency_ms if turn else 0.0,
            "detected_language": turn.detected_language if turn else "",
            "barge_in_count": self._barge_in_count,
            "total_turns": self._total_turns,
            "tool_calls": turn.tool_calls if turn else [],
            "language_history": self._language_history[-5:],
        }


# Global singleton
telemetry = TelemetryTracker()

