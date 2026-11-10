# ADR 0004: Sovereign Concurrency Guard and HTTP 429 Prevention

## Status
Accepted

## Context
When multiple parallel requests or audio chunks hit upstream sovereign voice endpoints simultaneously, upstream rate limiters trigger HTTP 429 Too Many Requests errors. Furthermore, retired API versions like `timbre-v2.0` cause degraded audio quality and API rejections.

## Decision
1. Implement a centralized asynchronous semaphore (`asyncio.Semaphore(1)`) with exponential backoff and jitter (`concurrency_guard.py`).
2. Enforce strict model version checks that proactively raise an explicit `ValueError` when deprecated models are requested.

## Consequences
* **Positive:** 0 concurrency collisions under high-frequency testing.
* **Positive:** Guaranteed enforcement of modern Gnani Timbre v3.0 / v2.5 streaming endpoints.
