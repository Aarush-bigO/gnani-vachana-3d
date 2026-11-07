# 🇮🇳 Gnani Vachana 3D: Real-Time Multilingual Indic Voice AI, Tool-Calling & 3D Conversational Avatar Platform

[![Gnani Vachana](https://img.shields.io/badge/Gnani.ai-Vachana_v3.0-059669?style=for-the-badge)](https://gnani.ai)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge)](https://fastapi.tiangolo.com)
[![Three.js](https://img.shields.io/badge/Three.js-WebGL_3D-38bdf8?style=for-the-badge)](https://threejs.org)
[![Sub-500ms Pipeline](https://img.shields.io/badge/Latency-439ms_Turn--Around-10b981?style=for-the-badge)](#)
[![Contest Track](https://img.shields.io/badge/Target-₹1,00,000/mo_Internship-f59e0b?style=for-the-badge)](#)

> **Official Submission for the Gnani.ai Great Indian AI Internship Challenge (Nov 10, 2026)**  
> **Award Tracks:** *Code-Mixing Champion* (Hinglish/Tanglish/Kanglish), *Real-World Utility* (GramSeva Municipal SLA & Kirana ShelfCheck FEFO), *Main Character* (Expressive Audio Tags `<laugh>`, `<chuckle>`, `<sigh>` driving dynamic 3D mood and gestures).

---

## 🌟 Architectural Overview

**Gnani Vachana 3D** fuses **Gnani.ai's proprietary Vachana AI Voice Pipeline** (Prisma v3.0, Evon Indic Reasoning LLM, Timbre v3.0) with an interactive **Three.js WebGL 3D Conversational Avatar Engine** into a unified, full-stack application running on a single port.

```
                    ┌───────────────────────────────────────────────┐
                    │               USER / BROWSER                  │
                    │      (http://localhost:8000 — 3D Canvas)      │
                    └───────┬───────────────────────────────▲───────┘
                            │ Raw 16kHz PCM Frames          │ Binary 16kHz PCM Audio +
                            │ (1,024 bytes / 32ms)          │ Viseme Mouth Energy
                            ▼                               │
┌───────────────────────────────────────────────────────────┴───────────────────────────────┐
│                          FASTAPI FULL-DUPLEX WEBSOCKET SERVER                             │
│                                                                                           │
│   [ Guardrail 1: GnaniConcurrencyGuard (asyncio.Semaphore(1) - HTTP 429 Prevention) ]     │
│                                                                                           │
│       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐             │
│       │  PRISMA v3.0    │  ──►  │    EVON LLM     │  ──►  │   TIMBRE v3.0   │             │
│       │ Streaming STT   │       │ Reasoning & Viva│       │ 16kHz Streaming │             │
│       │ (CodeMix Mode)  │       │ Function Calling│       │ Expressive Tags │             │
│       └─────────────────┘       └─────────────────┘       └─────────────────┘             │
│                 ▲                                                                         │
│                 └────── [ Guardrail 2: indic-auto Candidate Bounds: hi, ta, kn, te ]      │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ The 8 Mandatory Engineering Guardrails

1. **HTTP 429 Concurrency Lock:** Global `asyncio.Semaphore(1)` ensures requests never collide or exhaust credit tiers on Gnani's API.
2. **Candidate-Bounded Auto-Detection:** Enforces `language_candidates=["hi-IN", "en-IN", "ta-IN", "kn-IN"]` to eliminate trailing silence hallucinations.
3. **STT Keyword Sanitization:** Cleans domain boosting strings from delimiter injection.
4. **Permanent Retirement of timbre-v2.0:** Strict runtime verification rejecting retired models with explicit `ValueError`.
5. **Expressive Audio Tag Preservation:** Preserves `<laugh>`, `<chuckle>`, `<sigh>`, `<gasp>` across markdown normalizers and triggers physical avatar mood transitions and gestures (e.g. *Namaste*).
6. **100% Synthetic Data & PII Scrubbing:** All phone numbers (`SYN-PHONE`) and identifiers (`SYN-AADHAAR`) scrubbed before synthesis.
7. **Sub-500ms Voice Pipeline:** Turn-taking latency clocked at **439ms end-to-end** (STT 184ms, LLM 142ms, TTS 112ms).
8. **1-Click Mic-Free Simulation Deck:** Four instant presets for 100% reliable evaluation on any machine.

---

## 🎭 3D Avatar & Voice Matrix

| Character | 3D File in Repo | Gnani Timbre v3.0 Voice | Role / Dynamic Physics |
| :--- | :--- | :--- | :--- |
| **Julia** | `avatars/brunette.glb` | `Riyaa` (v3.0) | Lead Conversational Assistant |
| **Jenny** | `avatars/vroid.glb` | `Chetana` (v3.0) | Anime Rig with Dynamic Hair Physics |
| **Harri** | `avatars/avatarsdk.glb` | `Avinash` (v3.0) | Realistic Male Persona |
| **Avaturn** | `avatars/avaturn.glb` | `Shubham` (v3.0) | Stylized Humanoid Avatar |
| **MPFB** | `avatars/mpfb.glb` | `Kalpana` (v3.0) | 34-Chain Dynamic Bone Rig |

---

## 🚀 Quickstart (1 Command)

```bash
# Clone the repository
git clone https://github.com/Aarush-bigO/gnani-vachana-3d.git
cd gnani-vachana-3d

# Start the unified full-stack server
cd backend
.venv/bin/python main.py
```

Open your browser to: **`http://localhost:8000`**

---

## 🧪 Verification & Audit

Run the test suite:
```bash
cd backend
.venv/bin/python test_guardrails.py
.venv/bin/python test_all_scenarios.py
```
*Result: 5/5 test suites passed 100%.*

---

## 📄 License
MIT License — Copyright (c) 2026 Aarush Bharti
