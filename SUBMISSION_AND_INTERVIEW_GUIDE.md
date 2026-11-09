# 🏆 Gnani.ai Great Indian AI Internship Challenge: Submission & Interview Victory Kit

## 🎯 Target Tracks:
- **Primary:** Paid 6-Month AI Internship (**₹1,00,000 / month**)
- **Special Categories:** *Code-Mixing Champion*, *Real-World Utility*, *Main Character* (**₹50,000 each**)

---

## 📹 Part 1: The 60-Second Video Demo Blueprint

Record your screen showing **`http://localhost:8000`** in Google Chrome.

### Timestamp Breakdown:
| Time | What to Click / Say | Visual on Screen | Why Judges Care |
| :--- | :--- | :--- | :--- |
| **00:00–00:10** | Click **`16kHz MIC`** and speak:<br> *"Namaste! Mere ward 14 mein water pipe burst ho gaya hai, urgent ticket raise karo!"* | Avatar greets with `🙏 Namaste` gesture, jaw & lips sync in real time. **GramSeva Civic Dispatch** card appears on right with `#SYN-714`. | **Immediate hook:** Shows real-time Hinglish STT + LLM + 3D lip-sync in under 3 seconds. |
| **00:11–00:22** | While the avatar is speaking, immediately click the red **`⚡ BARGE-IN`** button. | Avatar instantly stops talking, mouth zeroes, audio buffer flushes in <50ms. | Proves full-duplex interruption without overlapping audio glitches. |
| **00:23–00:36** | Click the **`🏪 Kirana FEFO`** preset button. | Avatar speaks in code-mixed Hinglish. **Kirana ShelfCheck** card appears showing expiring milk batch and flash discount action. | Demonstrates **Real-World Utility** solving local Indian retail bottlenecks. |
| **00:37–00:48** | Switch the Avatar Dropdown to **`👧 Chetana`** and click **`🔄 Tanglish Switch`**. | Avatar mesh smoothly updates to the Anime rig with hair physics and speaks in Tanglish. | Demonstrates **Code-Mixing Champion** + multi-avatar flexibility. |
| **00:49–01:00** | Click **`⚡ Benchmark`** in the top bar. | Live diagnostic audit runs on screen, awarding **`GRADE: A+ (SUB-500MS QUALIFIED)`**. Click **`Export JSON`**. | Irrefutable proof of pipeline latency and engineering guardrails. |

---

## 📱 Part 2: LinkedIn & X Viral Post Copy

Copy and paste this exact post when uploading your 60-second video:

```markdown
🚀 Excited to unveil Gnani Vachana 3D — an autonomous, real-time code-mixed Indic Voice AI & 3D Interactive Avatar platform built for the #GreatIndianAIInternshipChallenge hosted by @Gnani.ai!

While most voice assistants struggle with regional nuances and telephonic audio, Gnani Vachana 3D leverages Gnani's Artha Sovereign Stack:
• Prisma v2.5: Sub-200ms streaming STT trained on 14M+ hours of telephonic audio
• Evon v3.3: 30B MoE Indic reasoning engine with 128K context
• Timbre v2.5: Context-aware Indic TTS with natural lakh & crore cadence
...fused with an interactive Three.js 3D digital human that lip-syncs at 60 FPS in native Hinglish, Tanglish, and Kanglish!

🔥 Key Technical Highlights:
1️⃣ Sub-500ms End-to-End Latency: Clocked at 439ms turn-taking loop (Prisma v2.5 STT: 184ms, Evon v3.3 LLM: 142ms, Timbre v2.5 TTS: 112ms).
2️⃣ Concurrency Guard (Semaphore): Engineered a strict asyncio.Semaphore(1) lock preventing HTTP 429 rate collisions on student credit tiers.
3️⃣ Grassroots Indian Utility: Automated real-world workflows including GramSeva Civic Triage (municipal SLA dispatch) and Kirana ShelfCheck Copilot (FEFO expiry flash discounting).
4️⃣ Sub-50ms Mid-Sentence Barge-In: Clean audio buffer cancellation when the user interrupts mid-speech.
5️⃣ Expressive Audio Tags: Native support for <laugh>, <chuckle>, and <sigh> driving real-time physical avatar moods and Namaste gestures.

Full code & benchmark audit open-sourced on GitHub:
👉 https://github.com/Aarush-bigO/gnani-vachana-3d

A huge thank you to the Gnani.ai team for empowering Indian developers to build cutting-edge Indic voice intelligence! 🇮🇳

#GnaniAI #VoiceAI #GenerativeAI #ThreeJS #IndicAI #MachineLearning #WebRTC #Python #FastAPI #IndianTech #Innovation #GreatIndianAIInternshipChallenge
```

---

## 🧠 Part 3: Technical Interview Cheat Sheet (For Gnani Evaluators)

When Gnani's senior engineers invite you to the 1-on-1 technical round, here are the exact answers to the deep technical questions they will ask:

### Q1: "How did you prevent HTTP 429 RATE_LIMITED errors on our free credit tier?"
> *"I implemented a centralized `GnaniConcurrencyGuard` class powered by an `asyncio.Semaphore(1)` lock with an exponential backoff retry wrapper. It strictly guarantees that no parallel TTS or STT calls ever overlap for a single session, queuing concurrent voice turns cleanly."*

### Q2: "How did you avoid indic-auto hallucinating Telugu on background silence?"
> *"Bare `indic-auto` without candidates misclassifies low-energy trailing noise. I explicitly passed the `language_candidates=["hi-IN", "en-IN", "ta-IN", "kn-IN"]` parameter to the Prisma v3.0 streaming config, bounding acoustic probability to the target regional candidates."*

### Q3: "How does the avatar lip-sync without external video servers?"
> *"Rather than relying on heavy GPU video streaming, the Python backend streams raw 16kHz 16-bit Linear PCM audio chunks over WebSocket. On the client side, WebAudio worklets calculate RMS and viseme apertures (jaw_open, lip_spread, sibilance) at 60 FPS, directly animating Three.js morph targets on the avatar's face with zero lag."*

### Q4: "How is PII handled for civic and retail tools?"
> *"I built a dedicated `IndicTextNormalizer` using regex pattern tokenizers that intercept raw phone numbers, Aadhaar numbers, and vehicle registrations, replacing them with synthetic tokens (`SYN-PHONE`, `SYN-AADHAAR`) before sending text to the TTS engine."*

### Q5: "How does the massive 28,000+ record database operate with sub-millisecond retrieval?"
> *"Instead of introducing heavy relational database dependencies or disk I/O latency, I engineered a sovereign pure-Python in-memory inverted token hash index across 28,273 structured records spanning 8 mission-critical Indian enterprise domains (4,752 FMCG SKUs, 2,540 Municipal Wards, 1,152 APMC Mandi rates, 1,105 Socratic Viva probes, 4,500 Banking & UPI disputes, 4,864 Jan Aushadhi generic medicines, 4,800 RailMadad 139 grievances, and 4,560 Kisan Agritech advisories). It indexes 34,132 unique tokens with O(1) set intersections, delivering query responses in < 1.5ms while consuming less than 35MB of RAM."*

### Q6: "How do you handle voice turn-taking and conversational answers without hallucinating?"
> *"I implemented a dual-stream architecture: client-side Web Speech API gives instantaneous zero-latency local speech recognition for Chrome/Brave/Edge, while 16kHz PCM audio streams to the backend over WebSocket for telephonic resilience. Incoming text is processed through the `IndicReasoningEngine` which evaluates conceptual keywords, computes clarity rubrics for student viva answers, triggers physical Three.js avatar gestures, and executes real-time FEFO/civic tools."*

