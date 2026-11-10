# Contributing to Gnani Vachana 3D

Thank you for your interest in contributing to **Gnani Vachana 3D** — Bharat's premier sovereign Indic 3D voice AI and digital human platform.

## Development Workflow

1. **Fork and Clone:**
   ```bash
   git clone https://github.com/Aarush-bigO/gnani-vachana-3d.git
   cd gnani-vachana-3d
   ```

2. **Set Up Python Virtual Environment:**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   ```bash
   cp backend/.env.example backend/.env
   # Add your Gnani API Key
   ```

4. **Verify Mandatory Engineering Guardrails:**
   ```bash
   python test_guardrails.py
   python test_all_scenarios.py
   ```

## Contribution Principles
* **Sovereignty First:** All core components must prioritize indigenous, low-latency Indian AI infrastructure.
* **Preserve Indic Unicode:** Any changes to NLP tokenization must strictly retain Indic characters in `\u0900-\u0D7F`.
* **Latency Budget:** Turn-taking latency must remain under 500ms; barge-in under 50ms.
* **Synthetic Data Guardrail:** Do not commit raw user credentials, real phone numbers, or real Aadhaar numbers.
