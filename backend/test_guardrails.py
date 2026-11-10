"""
BhashaSwarm 3D — Unit Test Suite for Engineering Guardrails
============================================================
Verifies:
1. IndicTextNormalizer removes markdown (*, #, `, ~), expands ₹ currency,
   spaces out ticket codes, scrubs 10-digit phone and 12-digit Aadhaar PII,
   and preserves valid Timbre v3.0 audio tags (<laugh>, <chuckle>, etc.).
2. Voice-model registry raises ValueError on retired 'timbre-v2.0',
   validates timbre-v3.0 and timbre-v2.5 voices, and handles fallbacks.
3. STT keyword sanitizer strips '<|' and '|>' prompt-injection tokens.
4. Concurrency guard semaphore enforces 1-slot lock and increments collision counter.
5. All 3 synthetic tools execute cleanly and return structured cards + spoken summaries.
"""
import asyncio
from config import settings, sanitize_stt_keywords, TIMBRE_V30_VOICES, TIMBRE_V25_VOICES
from normalizer import IndicTextNormalizer, PIISanitizer
from concurrency_guard import GnaniConcurrencyGuard
from tools import execute_agent_tool, SYNTHETIC_INVENTORY


def test_voice_model_validation():
    print("\n--- Testing Voice Model Registry (Guardrail #4) ---")
    # Test 1: timbre-v2.0 must raise ValueError
    try:
        settings.validate_voice_model("timbre-v2.0", "Riyaa")
        assert False, "Should have raised ValueError for retired timbre-v2.0"
    except ValueError as e:
        assert "retired" in str(e).lower()
        print("✓ Retired timbre-v2.0 successfully raised ValueError")

    # Test 2: timbre-v3.0 with valid voice
    m, v = settings.validate_voice_model("timbre-v3.0", "Riyaa")
    assert m == "timbre-v3.0" and v == "Riyaa"
    print("✓ timbre-v3.0 with Riyaa validated")

    # Test 3: timbre-v3.0 with invalid voice falls back to Riyaa
    m, v = settings.validate_voice_model("timbre-v3.0", "NonExistentVoice")
    assert m == "timbre-v3.0" and v == "Riyaa"
    print("✓ timbre-v3.0 fallback to default voice validated")

    # Test 4: timbre-v2.5 with valid voice
    m, v = settings.validate_voice_model("timbre-v2.5", "Pranav")
    assert m == "timbre-v2.5" and v == "Pranav"
    print("✓ timbre-v2.5 with Pranav validated")


def test_stt_keyword_sanitization():
    print("\n--- Testing STT Keyword Sanitization (Guardrail #3) ---")
    dirty_keywords = ["normal_keyword", "<|special_token|>", "foo<|bar", "baz|>"]
    cleaned = sanitize_stt_keywords(dirty_keywords)
    assert "<|" not in " ".join(cleaned)
    assert "|>" not in " ".join(cleaned)
    assert "normal_keyword" in cleaned
    assert "special_token" in cleaned
    print("✓ STT keywords sanitized from prompt-injection delimiters")


def test_indic_text_normalizer():
    print("\n--- Testing Indic Text Normalizer & PII (Guardrails #5 & #6) ---")
    # Test Markdown stripping
    sample_md = "**Urgent Notice**: Please check `#SYN402` and *review* `code` immediately!"
    cleaned = IndicTextNormalizer.normalize_for_tts(sample_md)
    assert "*" not in cleaned
    assert "`" not in cleaned
    assert "ID S Y N 4 0 2" in cleaned
    print(f"✓ Markdown stripped & ticket formatted: '{cleaned}'")

    # Test Currency expansion
    sample_curr = "Total cost is ₹45,000 for the renewal and Rs. 1,25,000 for infrastructure."
    cleaned_curr = IndicTextNormalizer.normalize_for_tts(sample_curr)
    assert "₹" not in cleaned_curr
    assert "rupees" in cleaned_curr.lower()
    print(f"✓ Currency expanded: '{cleaned_curr}'")

    # Test Audio Tag preservation
    sample_tags = "<chuckle> Bahut badhiya! <laugh> Yeh sunkar maza aa gaya. <sigh> Lekin dhyan rakhein. <gasp> Yeh kya hua!"
    cleaned_tags = IndicTextNormalizer.normalize_for_tts(sample_tags)
    assert "<chuckle>" in cleaned_tags
    assert "<laugh>" in cleaned_tags
    assert "<sigh>" in cleaned_tags
    assert "<gasp>" in cleaned_tags
    print(f"✓ Expressive audio tags preserved: '{cleaned_tags}'")

    # Test PII Sanitization
    sample_pii = "Contact me at 9876543210 or check Aadhaar 1234 5678 9012 for verification."
    cleaned_pii = IndicTextNormalizer.normalize_for_tts(sample_pii)
    assert "9876543210" not in cleaned_pii
    assert "SYN-DEMO-PHONE" in cleaned_pii
    assert "1234 5678 9012" not in cleaned_pii
    assert "SYN-DEMO-AADHAAR" in cleaned_pii
    print(f"✓ PII successfully sanitized into synthetic tokens: '{cleaned_pii}'")


def test_synthetic_tools():
    print("\n--- Testing Synthetic Tools (Guardrail #6 & Contest Utility) ---")
    # 1. Civic Dispatch Tool
    civic_res = execute_agent_tool("dispatch_gramseva_ticket", {
        "ward": "Ward 4 - MP Nagar Synthetic Zone",
        "category": "power_outage",
        "severity": "CRITICAL_P1",
        "description": "Transformer spark ho raha hai"
    })
    assert civic_res["card_type"] == "CIVIC_DISPATCH"
    assert "SYN" in civic_res["ticket_id"]
    assert "spoken_summary" in civic_res
    print(f"✓ Civic dispatch card generated: {civic_res['ticket_id']} - {civic_res['sla_eta']}")

    # 2. Kirana Inventory Tool
    kirana_res = execute_agent_tool("query_kirana_inventory", {
        "sku": "amul_taaza_500ml",
        "query_type": "expiry_alert"
    })
    assert kirana_res["card_type"] == "KIRANA_COPILOT"
    assert kirana_res["current_stock"] == 42
    assert "spoken_summary" in kirana_res
    print(f"✓ Kirana inventory card generated: {kirana_res['sku']} - Action: {kirana_res['recommended_action']}")

    # 3. Socratic Viva Tool
    viva_res = execute_agent_tool("evaluate_socratic_viva", {
        "topic": "Deadlock vs Starvation",
        "student_answer": "Deadlock happens when processes wait for each other in circular fashion.",
        "clarity_score": 88
    })
    assert viva_res["card_type"] == "SOCRATIC_VIVA"
    assert "next_socratic_probe" in viva_res
    assert "mastery_breakdown" in viva_res
    print(f"✓ Socratic viva card generated: Score {viva_res['clarity_score']}% - Probe: {viva_res['next_socratic_probe'][:50]}...")

    # 4. Banking & UPI Dispute Tool
    bank_res = execute_agent_tool("resolve_upi_banking_dispute", {
        "query": "Mera 5000 rupaye deduct ho gaya lekin transaction fail ho gaya"
    })
    assert bank_res["card_type"] == "BANKING_DISPUTE"
    assert "DISP" in bank_res["dispute_id"]
    assert "reversal_sla" in bank_res
    print(f"✓ Banking dispute card generated: {bank_res['dispute_id']} - {bank_res['reversal_sla']}")

    # 5. Jan Aushadhi Medicine Tool
    med_res = execute_agent_tool("query_jan_aushadhi_medicine", {
        "medicine": "Dolo 650"
    })
    assert med_res["card_type"] == "JAN_AUSHADHI"
    assert "Savings" in med_res["savings"]
    assert "jan_aushadhi_mrp" in med_res
    print(f"✓ Jan Aushadhi medicine card generated: {med_res['generic_medicine']} ({med_res['savings']})")

    # 6. RailMadad 139 Grievance Tool
    rail_res = execute_agent_tool("dispatch_railmadad_grievance", {
        "grievance": "Vande Bharat AC cooling issue"
    })
    assert rail_res["card_type"] == "RAILMADAD_139"
    assert "MADAD" in rail_res["railmadad_ticket"]
    assert "sla_target" in rail_res
    print(f"✓ RailMadad grievance card generated: {rail_res['railmadad_ticket']} - {rail_res['train']}")

    # 7. Kisan Agritech Advisory Tool
    agri_res = execute_agent_tool("diagnose_crop_agritech_issue", {
        "query": "Dhaan me blast rog patta jhulsa"
    })
    assert agri_res["card_type"] == "KISAN_ADVISORY"
    assert "KISAN" in agri_res["advisory_id"]
    assert "recommended_treatment" in agri_res
    print(f"✓ Kisan agritech advisory card generated: {agri_res['advisory_id']} - {agri_res['disease_identified']}")

    # 8. armour365™ Cyber Threat & Scam Interception Tool
    scam_res = execute_agent_tool("intercept_armour365_scam_call", {
        "query": "Digital arrest scam call CBI"
    })
    assert scam_res["card_type"] == "ARMOUR365_FRAUD"
    assert "ARMOUR" in scam_res["scam_id"]
    assert "1930" in scam_res["helpline"]
    print(f"✓ armour365 scam card generated: {scam_res['scam_id']} - {scam_res['threat_title']}")


async def async_test_concurrency_guard():
    print("\n--- Testing Concurrency Guard Semaphore (Guardrail #1) ---")
    guard = GnaniConcurrencyGuard()

    # Slot 1 holds lock for 0.1s
    async def task_holder():
        async with guard.acquire_slot("task_holder"):
            await asyncio.sleep(0.1)

    # Slot 2 tries to acquire immediately and will trigger collision counter
    async def task_waiter():
        await asyncio.sleep(0.01) # ensure task_holder runs first
        async with guard.acquire_slot("task_waiter"):
            await asyncio.sleep(0.01)

    await asyncio.gather(task_holder(), task_waiter())

    telemetry = guard.get_telemetry()
    assert telemetry["total_served"] == 2
    assert telemetry["prevented_429s"] >= 1
    print(f"✓ Concurrency Guard prevented {telemetry['prevented_429s']} HTTP 429 collision(s), served {telemetry['total_served']} requests safely.")


def run_all_tests():
    test_voice_model_validation()
    test_stt_keyword_sanitization()
    test_indic_text_normalizer()
    test_synthetic_tools()
    asyncio.run(async_test_concurrency_guard())
    print("\n==========================================")
    print("🎯 ALL 5 GUARDRAIL TEST SUITES PASSED 100%")
    print("==========================================\n")


if __name__ == "__main__":
    run_all_tests()
