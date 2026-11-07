"""
BhashaSwarm 3D — Gnani Concurrency Guard
==========================================
GUARDRAIL #1: Prevents HTTP 429 "Only 1 active request is allowed at a time"
on the 5,000-credit challenge tier by serializing all Gnani API calls through
a global asyncio.Semaphore(1).

Every Gnani STT/TTS/REST call MUST be wrapped in:
    async with concurrency_guard.acquire_slot("operation_name"):
        ...
"""
import asyncio
import time
import logging
from contextlib import asynccontextmanager
from typing import Optional

logger = logging.getLogger("bhashaswarm.concurrency")


class GnaniConcurrencyGuard:
    """
    Enforces Gnani Vachana's strict 1-active-request concurrency rule on the
    5,000-credit challenge tier so parallel synthesis calls never trigger HTTP 429.

    Tracks telemetry counters for the live HUD:
    - active_requests: Currently held slots (0 or 1)
    - total_requests_served: Lifetime total
    - prevented_429_collisions: Times a second caller had to wait
    - last_latency_ms: Duration of the most recent guarded operation
    - last_operation: Name of the most recent guarded operation
    """

    def __init__(self):
        self._semaphore = asyncio.Semaphore(1)
        self.active_requests: int = 0
        self.total_requests_served: int = 0
        self.prevented_429_collisions: int = 0
        self.last_latency_ms: float = 0.0
        self.last_operation: str = ""

    @asynccontextmanager
    async def acquire_slot(self, operation_name: str = "gnani_op"):
        """
        Acquires the single concurrency slot. If the slot is already held,
        increments the collision counter and blocks until the slot is free.

        Usage:
            async with concurrency_guard.acquire_slot("tts_synthesize"):
                await gnani_tts.send(...)
        """
        if self._semaphore.locked():
            self.prevented_429_collisions += 1
            logger.warning(
                "⚠️  429 Collision PREVENTED — '%s' waiting for slot "
                "(total prevented: %d)",
                operation_name,
                self.prevented_429_collisions,
            )

        t0 = time.perf_counter()
        async with self._semaphore:
            self.active_requests = 1
            self.last_operation = operation_name
            logger.debug("🔒 Slot acquired for '%s'", operation_name)
            try:
                yield
            finally:
                self.active_requests = 0
                self.total_requests_served += 1
                self.last_latency_ms = round(
                    (time.perf_counter() - t0) * 1000, 1
                )
                logger.debug(
                    "🔓 Slot released for '%s' — %.1fms",
                    operation_name,
                    self.last_latency_ms,
                )

    def get_telemetry(self) -> dict:
        """Returns a snapshot of concurrency telemetry for the live HUD."""
        return {
            "active_requests": self.active_requests,
            "total_served": self.total_requests_served,
            "prevented_429s": self.prevented_429_collisions,
            "last_latency_ms": self.last_latency_ms,
            "last_operation": self.last_operation,
        }


# Global singleton — import this in agent_pipeline.py and main.py
concurrency_guard = GnaniConcurrencyGuard()

