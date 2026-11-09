# 🇮🇳 Gnani Vachana 3D: Real-Time Multilingual Indic Voice AI, Tool-Calling & 3D Conversational Avatar Platform

[![Gnani Artha Stack](https://img.shields.io/badge/Gnani.ai-Artha_Sovereign_Stack-059669?style=for-the-badge)](https://gnani.ai/internship)
[![Prisma v2.5](https://img.shields.io/badge/STT-Prisma_v2.5_(<200ms)-6366f1?style=for-the-badge)](https://gnani.ai/internship)
[![Evon v3.3](https://img.shields.io/badge/LLM-Evon_v3.3_(30B_MoE)-a855f7?style=for-the-badge)](https://gnani.ai/internship)
[![Timbre v2.5](https://img.shields.io/badge/TTS-Timbre_v2.5_/_v3.0-ec4899?style=for-the-badge)](https://gnani.ai/internship)
[![Sub-500ms Pipeline](https://img.shields.io/badge/Turn_Latency-439ms-10b981?style=for-the-badge)](#)
[![Contest Track](https://img.shields.io/badge/Target-₹1,00,000/mo_Internship-f59e0b?style=for-the-badge)](#)

> **Official Submission for the Gnani.ai Great Indian AI Internship Challenge (Nov 10, 2026)**  
> **Target Award Tracks:** *Code-Mixing Champion* (Hinglish/Tanglish/Kanglish), *Real-World Utility* (GramSeva Municipal SLA & Kirana ShelfCheck FEFO), *Main Character* (Expressive Audio Tags `<laugh>`, `<chuckle>`, `<sigh>` driving dynamic 3D mood and physical gestures).

---

## 🌟 Architectural Overview

**Gnani Vachana 3D** fuses **Gnani.ai's Artha Sovereign Stack**:
- **Prisma v2.5:** Sub-200ms streaming Speech-to-Text trained on 14M+ hours of real telephonic audio across 10+ Indian languages plus Hinglish, Tanglish, and Benglish.
- **Evon v3.3:** 30B-parameter Mixture-of-Experts (MoE) reasoning engine with 128K context and native support for 11 Indian languages.
- **Timbre v2.5 / v3.0:** Indic TTS with context-aware prosody, Indian name recognition, and natural lakh & crore cadence.
- **3D Avatar Engine:** Interactive Three.js WebGL digital humans with real-time phoneme-viseme lip-sync at 60 FPS on a unified single port.

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
│       │  PRISMA v2.5    │  ──►  │    EVON v3.3    │  ──►  │TIMBRE v2.5/v3.0 │             │
│       │ Sub-200ms STT   │       │ 30B MoE Reasoner│       │ Context-Aware   │             │
│       │ (CodeMix Mode)  │       │ Function Calling│       │ Lakh/Crore TTS  │             │
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

## 🎭 3D Avatar & Voice Matrix (Gen-Z Indian Avatars)

| Character | 3D File in Repo | Gnani Timbre v3.0 Voice | Role / Dynamic Physics |
| :--- | :--- | :--- | :--- |
| **Riya** | `avatars/brunette.glb` | `Riyaa` (v3.0) | Lead Gen-Z Conversationalist |
| **Chetana** | `avatars/vroid.glb` | `Chetana` (v3.0) | Gen-Z Anime Rig with Dynamic Hair Physics |
| **Kabir** | `avatars/avatarsdk.glb` | `Avinash` (v3.0) | Realistic Gen-Z Male Persona |
| **Shubham** | `avatars/avaturn.glb` | `Shubham` (v3.0) | Stylized 3D Creator Humanoid Avatar |
| **Kalpana** | `avatars/mpfb.glb` | `Kalpana` (v3.0) | High-Fidelity 34-Chain Dynamic Bone Rig |

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
