# ADR 0002: Sub-50ms Conversational Barge-In Protocol

## Status
Accepted

## Context
Natural human conversation involves frequent mid-sentence interruptions. If a voice AI agent continues speaking over the user, the perceived quality plummets. Waiting for a full HTTP request-response cycle causes noticeable 200ms+ halting lag.

## Decision
Implement a client-initiated WebSocket event `{"type": "barge_in"}` over `/ws/voice`. The client audio context immediately flushes its queued PCM buffer, pauses the AudioWorklet player, transitions the 3D avatar mouth to a neutral listening pose, and commands the backend server to abort ongoing TTS synthesis.

## Consequences
* **Positive:** Interruption latency is under 50ms, delivering instant, fluid conversational turn-taking.
* **Positive:** Eliminates wasteful downstream TTS generation and network bandwidth.
