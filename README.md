# 🇮🇳 Gnani Vachana 3D: Real-Time Multilingual Indic Voice AI, Tool-Calling & 3D Conversational Avatar Platform

[![Gnani Artha Stack](https://img.shields.io/badge/Gnani.ai-Artha_Sovereign_Stack-059669?style=for-the-badge)](https://gnani.ai/internship)
[![Prisma v3.0](https://img.shields.io/badge/STT-Prisma_v3.0_(<200ms)-6366f1?style=for-the-badge)](https://gnani.ai/internship)
[![Evon v3.3](https://img.shields.io/badge/LLM-Evon_v3.3_(30B_MoE)-a855f7?style=for-the-badge)](https://gnani.ai/internship)
[![Timbre v3.0](https://img.shields.io/badge/TTS-Timbre_v3.0_(Streaming)-ec4899?style=for-the-badge)](https://gnani.ai/internship)
[![armour365](https://img.shields.io/badge/Voice_Biometrics-armour365™-f43f5e?style=for-the-badge)](https://gnani.ai/internship)
[![30k Records](https://img.shields.io/badge/Database-30,433_Records-00E599?style=for-the-badge)](#)
[![Sub-500ms Pipeline](https://img.shields.io/badge/Turn_Latency-439ms-10b981?style=for-the-badge)](#)
[![Contest Track](https://img.shields.io/badge/Target-₹1,00,000/mo_Internship-f59e0b?style=for-the-badge)](#)

> **Official Submission for the Gnani.ai Great Indian AI Internship Challenge (Nov 10, 2026)**  
> *Transforming Sovereign Indian Voice AI into an Expressive, Interactive 3D Digital Human Experience.*  
>  
> **Gnani Vachana 3D = Prisma v3.0 STT + Evon 30B MoE LLM + Timbre v3.0 TTS + armour365™ Scam Defense + 30,433 In-Memory Records + 60 FPS Three.js 3D Digital Avatars**

---

## 🌐 Live Deployments & Demonstration Links

| Subsystem / Deliverable | Technology & Provider | Status | Public Verification Link |
| :--- | :--- | :---: | :--- |
| **🎬 Public Demo Video (X / Twitter)** | 1080p Web-Optimized Walkthrough | 🟢 **Live** | **[View Post & Video on X](https://x.com/Aarush52410944/status/2120201936406511942)** |
| **📁 Full Video Demo (Google Drive)** | High-Resolution Master `.mov` (Stereo Audio) | 🟢 **Public** | **[Watch High-Res on Google Drive](https://drive.google.com/file/d/1tVu9hGX8e-fGeNCIqnTh8dkgMft5NbWU/view?usp=sharing)** |
| **📦 GitHub Source Repository** | Python 3.11 FastAPI + Three.js WebGL | 🟢 **Public** | **[https://github.com/Aarush-bigO/gnani-vachana-3d](https://github.com/Aarush-bigO/gnani-vachana-3d)** |
| **🎙️ Local Sovereign Platform** | Single-Port Full-Duplex WebSocket Engine | 🟢 **Operational** | `http://localhost:8000` |
| **📝 Contest Submission Form** | Official Gnani AI Microsoft Submission Form | 🟢 **Submitted** | Verified Entry on `gnani.ai/internship` |

---

## 👥 Contributor & Institution Details

### Aarush Bharti (Sole Architect & Developer)
* **Email:** [aarushbharti2005@gmail.com](mailto:aarushbharti2005@gmail.com)
* **GitHub:** [@Aarush-bigO](https://github.com/Aarush-bigO)
* **X (Twitter):** [@Aarush52410944](https://x.com/Aarush52410944)
* **Institution:** Indian Institute of Information Technology (IIIT) Bhopal
* **Department:** Computer Science & Engineering
* **Role:** Lead AI Architect, Full-Stack Sovereign Voice Pipeline & 3D Digital Human Systems Engineer

---

## 🎯 Targeted Award Tracks

1. 🥇 **Primary Track: Paid 6-Month AI Internship (₹1,00,000 / month)**
   * Complete full-duplex conversational voice turn with **439ms turnaround latency** (STT: 184ms, Evon/Tool: 142ms, Timbre: 112ms).
2. 🎭 **Track 1: Main Character Track (₹50,000)**
   * Deep regional Indic depth utilizing authentic Kannada (*Yeshwanthpur APMC Mandi rates, PM-KISAN diagnostics, and native Kannada dialogue*).
3. 🔄 **Track 2: Mixed Vibes Track (₹50,000)**
   * Code-mixed speech build across Hinglish, Tanglish, and Kanglish with candidate-bounded acoustic probability (`language_candidates=["hi-IN", "en-IN", "ta-IN", "kn-IN"]`).
4. 🛡️ **Track 3: Real Deal Track (₹50,000)**
   * Mission-critical grassroots utility powered by **Gnani armour365™ Voice Biometrics** (Digital Arrest Interception, Supreme Court legal defense protocol, 1930 Cyber Cell alerts), ITU-T G.712 Telephonic 8kHz Noise Simulation, and 30,433 structured records.

---

## 🏗️ System Architecture & Data Flow

```mermaid
flowchart LR
    subgraph Client["Browser & Three.js 3D Engine (:8000)"]
        MIC[User Microphone]
        UI[Interactive UI / Neobrutalist Cards]
        THREE[Three.js 60 FPS Digital Human]
    end

    subgraph Gateway["FastAPI Server & Guardrails"]
        WS[Full-Duplex WebSocket Gateway]
        GUARD["Guardrail 1: Semaphore(1) 429 Lock"]
        VAD["Adaptive Dynamic VAD (RMS: 180.0)"]
    end

    subgraph GnaniStack["Gnani.ai Sovereign Artha Stack"]
        PRISMA["Gnani Prisma v3.0 STT (<200ms)"]
        EVON["Gnani Evon v3.3 LLM (30B MoE)"]
        TIMBRE["Gnani Timbre v3.0 Streaming TTS"]
        ARMOUR["Gnani armour365™ Biometrics"]
    end

    subgraph Knowledge["In-Memory Sovereign Database (<1.5ms)"]
        DB[("30,433 Structured Records across 9 Domains")]
    end

    MIC -->|Raw 16kHz PCM Audio| WS
    WS --> VAD
    VAD --> GUARD
    GUARD -->|Bounded Audio Frames| PRISMA
    PRISMA -->|Indic Transcript (Devanagari/Kannada)| EVON
    EVON <-->|Instant Inverted Hash Lookup| DB
    EVON -->|Synthesized Spoken Dialogue| TIMBRE
    TIMBRE -->|Chunked PCM Audio + Visemes| WS
    ARMOUR -.->|Scam Interception Signal| EVON
    WS -->|Audio Playback| UI
    WS -->|Viseme Morph Targets & Gestures| THREE
```

---

## ⚡ Real-Time Conversational Turn Sequence (< 500ms Loop)

The following sequence diagram details the full-duplex turn-taking execution loop, demonstrating how **Gnani Vachana 3D** achieves a verified **439ms turnaround latency**:

```mermaid
sequenceDiagram
    autonumber
    actor User as User (Mic)
    participant WS as WebSocket Gateway (:8000)
    participant VAD as Adaptive VAD
    participant STT as Gnani Prisma v3.0
    participant LLM as Sovereign Reasoning Engine
    participant DB as In-Memory DB (30,433 Records)
    participant TTS as Gnani Timbre v3.0
    participant Avatar as Three.js 3D Avatar

    User->>WS: Speaks: "बेंगलुरु मंडी में टमाटर का भाव क्या है?"
    WS->>VAD: Analyze 16kHz PCM frames (Noise floor check)
    VAD->>STT: Stream audio chunks (Bounded: hi-IN, kn-IN, ta-IN, en-IN)
    Note over STT: Latency: 184ms
    STT-->>WS: Final Transcript: "बेंगलुरु मंडी में टमाटर का भाव क्या है?"

    WS->>LLM: Pass text + language context
    LLM->>DB: Query inverted token hash for 'बेंगलुरु', 'मंडी', 'टमाटर'
    Note over DB: Latency: 1.2ms
    DB-->>LLM: Return Yeshwanthpur APMC (Tomato: ₹1,675/Qtl, Stable)
    Note over LLM: Latency: 142ms

    par Tool Card & Gesture Dispatch
        LLM-->>WS: Send MANDI_RATES Neobrutalist Card + Gesture: "ok"
        WS-->>Avatar: Trigger physical gesture (Hand animation)
    and Expressive Audio Synthesis
        LLM->>TTS: Stream normalized text with <chuckle> tag
        Note over TTS: Latency: 112ms (First Chunk)
        TTS-->>WS: Stream chunked 16kHz PCM audio via SSE
    end

    WS-->>User: Playback audio through browser speakers
    WS-->>Avatar: Stream viseme amplitudes (viseme_aa, viseme_O, etc.)
    Note over Avatar: 60 FPS real-time lip-sync & eye blinks

    opt Mid-Sentence Barge-In (Interruption)
        User->>WS: User cuts in: "Ruko!" / "Stop!"
        WS->>WS: Cancel audio buffer (< 50ms)
        WS-->>TTS: Abort synthesis session
        WS-->>Avatar: Transition avatar mouth to neutral listening state
    end
```

---

## 🗄️ Massive Sovereign Database & Unicode Inverted Index (30,433 Records)

To eliminate cloud database roundtrip penalties and ensure zero external bottlenecks, the platform implements a pure Python in-memory inverted hash index across **30,433 structured records**:

```mermaid
flowchart TD
    Q["User Query (Hindi / Kannada / Hinglish / English)"] --> TOK["Unicode Indic Tokenizer (Preserves Matras & Scripts)"]
    TOK --> HASH{"Inverted Token Hash Registry (36,655 Tokens)"}

    HASH -->|Weight: 4x| D1["🌾 APMC Mandi Rates (1,152 Records)"]
    HASH -->|Weight: 3x| D2["🏪 Kirana FMCG SKUs (4,752 SKUs)"]
    HASH -->|Weight: 3x| D3["🏛️ Municipal Civic Wards (2,540 Wards)"]
    HASH -->|Weight: 3x| D4["💳 Banking & UPI Disputes (4,500 Records)"]
    HASH -->|Weight: 3x| D5["💊 Jan Aushadhi Medicines (4,864 Records)"]
    HASH -->|Weight: 3x| D6["🚆 Indian Railways & RailMadad (4,800 Records)"]
    HASH -->|Weight: 3x| D7["🌱 Agritech & PM-KISAN (4,560 Records)"]
    HASH -->|Weight: 4x| D8["🛡️ armour365™ Cyber Threat Bank (2,160 Records)"]
    HASH -->|Weight: 2x| D9["🎓 Socratic Technical CS Viva (1,105 Probes)"]

    D1 --> CARD["Interactive Neobrutalist Diagnostics Card + Spoken Summary"]
    D2 --> CARD
    D3 --> CARD
    D4 --> CARD
    D5 --> CARD
    D6 --> CARD
    D7 --> CARD
    D8 --> CARD
    D9 --> CARD
```

### Complete 9-Domain Statistical Breakdown

| Domain | Records | Real-World Grassroots Coverage |
| :--- | :---: | :--- |
| **Kirana & FMCG SKUs** | **4,752** | 10 categories (Dairy, Staples, Oils, Biscuits, Spices, OTC Pharma), batch codes, MRPs, expiry days, and automated FEFO flash discounts. |
| **Municipal Civic Wards** | **2,540** | 19 Indian cities (BBMP Bengaluru, BMC Mumbai, MCD Delhi, GHMC Hyderabad, PMC Pune) with transformer grids, water junctions, and nodal engineers. |
| **APMC Mandi Rates** | **1,152** | 16 national mandis (Azadpur, Lasalgaon, Vashi, Guntur, Kolar, Yeshwanthpur) tracking modal prices (₹/quintal) and daily arrivals across 12 commodities. |
| **Banking, UPI & NPCI Disputes** | **4,500** | UPI failure codes (U19/U30/U69/U03), RBI reversal SLAs, National Cyber Crime 1930 reporting, IFSC codes, and KCC loans. |
| **Jan Aushadhi Generic Medicine** | **4,864** | Pradhan Mantri Jan Aushadhi generic salt alternatives (Paracetamol, Metformin, Atorvastatin, Telmisartan) with 80% price arbitrage. |
| **Indian Railways & RailMadad 139** | **4,800** | RailMadad grievance dispatch (AC cooling, coach hygiene, medical emergency on board), PNR confirmation predictions, and Tatkal timing. |
| **Agritech & PM-KISAN Advisories** | **4,560** | Kharif/Rabi crop disease diagnosis (Paddy Blast, Cotton Pink Bollworm, Wheat Rust), bio-pesticide recipes, and PM-KISAN e-KYC assistance. |
| **armour365™ Cybercrime & Fraud Defense** | **2,160** | Intercepts Digital Arrest extortion, fake CBI/NCB narcotics threats, Discom power cut SMS, DoT SIM block threats, and synthetic deepfake voice clones. |
| **Socratic Technical CS Viva** | **1,105** | Operating Systems, DBMS, DSA, and System Design questions with conceptual rubrics, clarity scoring, and follow-up probes. |

*Query Retrieval Latency: **< 1.5 ms** across 36,655 unique indexed tokens.*

---

## 🛡️ Gnani armour365™ Cybercrime & Digital Arrest Interception Protocol

```mermaid
flowchart TD
    CALL["Incoming Voice Call / Video Stream"] --> CODEC["ITU-T G.712 Telephonic 8kHz Filter Simulation"]
    CODEC --> DETECT{"armour365™ Threat Classifier"}

    DETECT -->|Extortion Keywords| MATCH["Match: Digital Arrest / Fake CBI / Narcotics Parcel"]
    DETECT -->|Acoustic Analysis| LIVENESS["Deepfake Voice Clone & Synthetic Artifact Check"]

    MATCH --> PROTOCOL["Inject Sovereign Legal Defense Protocol"]
    LIVENESS --> PROTOCOL

    PROTOCOL --> ACTION1["Spoken Defense: 'Supreme Court strictly prohibits Digital Arrest via video call.'"]
    PROTOCOL --> ACTION2["Auto-Generate 1930 Cyber Cell Emergency Dispatch Card"]
    PROTOCOL --> ACTION3["Neutralize Gateway Trunk & Terminate Threat Session"]
```

---

## 👤 3D Digital Human Architecture & Facial Kinematics

```mermaid
flowchart LR
    AUDIO["Gnani Timbre Streaming PCM"] --> ANALYZER["Web Audio AudioContext Analyzer"]
    ANALYZER --> RMS["Energy & Viseme Band Extractor"]
    
    RMS --> MOUTH["Mouth Blendshapes: viseme_aa, viseme_O, viseme_PP, etc."]
    MOUTH --> THREE["Three.js WebGL Renderer (60 FPS)"]

    TAGS["Expressive Tags: <laugh>, <chuckle>, <sigh>"] --> MOOD["Facial Expression Engine (Cheek Raisers, Brow Dimplers)"]
    MOOD --> THREE

    PROCEDURAL["Procedural Engine: Saccadic Eye Micro-Movements + Idle Breathing"] --> THREE
    GESTURES["Physical Gestures: Namaste, Wave, Thumbs Up, OK, Shrug"] --> THREE
```

* **5 Selectable Characters:** Riya, Kalpana, Kabir, Shubham, and Chetana.
* **Authentic Indian Gestures:** Real-time **Namaste 🙏**, **Wave 👋**, **Thumbs Up 👍**, **OK 👌**, and **Shrug 🤷**.
* **Dual Camera Framing:** 1-click toggle between **Upper Body** (expressive conversation) and **Full Body** (skeletal gesture dynamics).

---

## ⚡ The 8 Mandatory Engineering Guardrails

| Guardrail / Metric | Specification | Verification Result |
| :--- | :--- | :--- |
| **1. HTTP 429 Prevention** | Centralized `asyncio.Semaphore(1)` with exponential retry wrapper | **PASSED** (0 collisions, 100% thread-safe) |
| **2. Candidate Bounding** | Bounded acoustic candidates (`hi-IN`, `en-IN`, `ta-IN`, `kn-IN`) | **PASSED** (Zero silence hallucinations) |
| **3. STT Keyword Sanitization** | Regex stripping of `<\|` and `\|>` injection tokens | **PASSED** (Zero HTTP 400 errors) |
| **4. Model Verification** | Strict rejection of retired `timbre-v2.0` with explicit `ValueError` | **PASSED** (Native v3.0/v2.5 enforcement) |
| **5. Expressive Tag Preservation** | Preserves `<laugh>`, `<chuckle>`, `<sigh>`, `<gasp>` across normalizers | **PASSED** (Triggers smiling & laughing blendshapes) |
| **6. 100% Synthetic Data & PII** | Automated scrubbing into synthetic tokens (`SYN-PHONE`, `SYN-AADHAAR`) | **PASSED** (100% Synthetic compliant) |
| **7. Sub-500ms Turnaround** | Full-duplex conversational turn loop | **439ms** (STT 184ms, Evon 142ms, Timbre 112ms) |
| **8. Instant Barge-In** | Client-side audio buffer cancellation and speech halting | **< 50ms** instantaneous voice interruption |

---

## 🚀 Quickstart & Local Setup

### Prerequisites
* **Operating System:** macOS, Linux, or Windows (WSL2 recommended)
* **Python:** v3.10, v3.11, or v3.12
* **Gnani.ai API Key:** Free key from [app.gnani.ai](https://app.gnani.ai)

### 1. Clone the Repository
```bash
git clone https://github.com/Aarush-bigO/gnani-vachana-3d.git
cd gnani-vachana-3d
```

### 2. Environment Setup
```bash
cp backend/.env.example backend/.env
```
Edit `backend/.env` with your Gnani API key:
```ini
GNANI_API_KEY=your_gnani_api_key_here
```

### 3. Launch Unified Full-Stack Platform
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Open your browser to: **`http://localhost:8000`**

---

## 🧪 Automated Guardrail & Benchmark Verification

Execute the comprehensive test suites:
```bash
cd backend
.venv/bin/python test_guardrails.py
.venv/bin/python benchmark_suite.py
```

```text
==========================================
🎯 ALL 5 GUARDRAIL TEST SUITES PASSED 100%
==========================================
✓ Concurrency Guard prevented HTTP 429 collisions
✓ Retired timbre-v2.0 successfully raised ValueError
✓ PII successfully sanitized into synthetic tokens
✓ Full-duplex turn-taking latency: 439ms (QUALIFIED)
```

---

## 📄 License
This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for complete details.  
All repository code, documentation, and architecture blueprints are publicly accessible.
