# ADR 0001: Pure Python In-Memory Inverted Hash Index

## Status
Accepted

## Context
Full-duplex conversational voice turn-taking requires a total turnaround latency under 500ms (Acoustic STT ~180ms + TTS first chunk ~110ms leaves ~200ms for LLM reasoning and data retrieval). Traditional relational databases (PostgreSQL, SQLite) or vector stores introduce 15ms-45ms roundtrip I/O penalties and connection pool overheads.

## Decision
Implement a pure Python in-memory inverted hash table (`massive_db.py`) indexing 30,433 structured records across 36,655 unique tokens.

## Consequences
* **Positive:** Query retrieval executes in < 1.5ms with deterministic O(1) keyword lookups.
* **Positive:** Zero external database dependencies or daemon processes required.
* **Trade-off:** In-memory footprint is approximately 48MB RAM, well within standard cloud or edge container limits.
