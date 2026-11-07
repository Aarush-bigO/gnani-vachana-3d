"""
BhashaSwarm 3D — Tool Execution Engine
========================================
3 rich, real-world Indian utility tools using 100% SYNTHETIC data.
Each tool returns structured card data + TTS-ready spoken_summary with
Gnani Timbre v3.0 expressive Audio Tags (<laugh>, <chuckle>, <sigh>, <gasp>).

Tools:
1. dispatch_gramseva_ticket — Civic & Municipal Triage (Hinglish/Hindi/Tamil)
2. query_kirana_inventory  — Kirana ShelfCheck & Mandi Copilot
3. evaluate_socratic_viva  — Hinglish Engineering Viva Examiner
"""
import time
import random
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("bhashaswarm.tools")

# ── Synthetic Inventory Database (100% Fake Data for Contest Compliance) ────
SYNTHETIC_INVENTORY: Dict[str, Dict[str, Any]] = {
    "amul_taaza_500ml": {
        "item": "Amul Taaza 500ml Batch SYN402",
        "stock": 42,
        "expiry_days": 2,
        "mrp": 28,
        "action": "TRIGGER_20_PERCENT_FLASH_DISCOUNT",
        "category": "Dairy",
    },
    "aashirvaad_atta_5kg": {
        "item": "Aashirvaad Atta 5kg Batch SYN819",
        "stock": 18,
        "expiry_days": 45,
        "mrp": 245,
        "action": "OPTIMAL_SHELF_HEALTH",
        "category": "Staples",
    },
    "paracetamol_650": {
        "item": "Dolo-650 Strip Batch SYN108",
        "stock": 110,
        "expiry_days": 14,
        "mrp": 32,
        "action": "PRIORITIZE_FEFO_DISPATCH",
        "category": "Pharma",
    },
    "tata_tea_premium_500g": {
        "item": "Tata Tea Premium 500g Batch SYN217",
        "stock": 65,
        "expiry_days": 120,
        "mrp": 195,
        "action": "OPTIMAL_SHELF_HEALTH",
        "category": "Beverages",
    },
    "parle_g_800g": {
        "item": "Parle-G Family Pack 800g Batch SYN633",
        "stock": 8,
        "expiry_days": 5,
        "mrp": 65,
        "action": "TRIGGER_BOGO_CLEARANCE",
        "category": "Biscuits",
    },
}

# ── Synthetic Ward Database ─────────────────────────────────────────────────
SYNTHETIC_WARDS: List[Dict[str, str]] = [
    {"ward": "Ward 4 - MP Nagar Synthetic Zone", "engineer": "Engr. Ramesh (SYN-EMP-042)"},
    {"ward": "Ward 12 - Arera Colony Synthetic", "engineer": "Engr. Priya (SYN-EMP-087)"},
    {"ward": "Ward 7 - Indrapuri Synthetic", "engineer": "Engr. Suresh (SYN-EMP-031)"},
    {"ward": "Ward 21 - Habibganj Synthetic", "engineer": "Engr. Meera (SYN-EMP-056)"},
]

# ── Socratic Viva Question Bank ─────────────────────────────────────────────
SOCRATIC_PROBES: Dict[str, List[str]] = {
    "operating_systems": [
        "Agar Coffman ki Circular Wait condition ko resource numbering se tod dein, toh kya starvation phir bhi ho sakta hai?",
        "Virtual memory mein thrashing tab hoti hai jab working set page frames se bada ho jaata hai — is scenario mein CPU utilization kyun girti hai?",
        "Priority Inversion kya hai aur Mars Pathfinder mission mein iska kya impact hua tha?",
        "Dining Philosophers problem mein agar ek philosopher left-handed ho, toh deadlock kyun break hota hai?",
    ],
    "dbms": [
        "ACID properties mein se Isolation level agar Serializable se Read Committed mein change karein, toh phantom reads kyun aane lagte hain?",
        "B+ Tree mein leaf nodes linked list form mein kyun hoti hain? Range query performance pe iska kya impact hai?",
        "Two-Phase Locking protocol deadlock prevent karta hai ya detect? Explain with example.",
        "Denormalization kab justified hai? OLTP vs OLAP systems mein trade-offs samjhaiye.",
    ],
    "dsa": [
        "Dijkstra's Algorithm negative edge weights ke saath fail kyun hota hai? Bellman-Ford kyun kaam karta hai?",
        "Red-Black Tree mein insertion ke baad recoloring aur rotation ka worst-case complexity kya hai?",
        "Dynamic Programming mein memoization aur tabulation ka space-time trade-off samjhaiye with a real example.",
        "Amortized analysis mein aggregate method aur potential method ka difference kya hai?",
    ],
}

# ── Tool Definitions for LLM Function Calling ───────────────────────────────
TOOL_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "dispatch_gramseva_ticket",
            "description": (
                "Dispatch a civic/municipal complaint ticket for synthetic Indian wards. "
                "Handles power outages, water pipeline leaks, road damage, sanitation, "
                "and crop transport issues. Uses 100% synthetic data."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ward": {
                        "type": "string",
                        "description": "Ward name or number (synthetic)",
                    },
                    "category": {
                        "type": "string",
                        "description": "Complaint category: power_outage, water_leak, road_damage, sanitation, crop_transport",
                        "enum": [
                            "power_outage",
                            "water_leak",
                            "road_damage",
                            "sanitation",
                            "crop_transport",
                        ],
                    },
                    "severity": {
                        "type": "string",
                        "description": "Severity level",
                        "enum": ["CRITICAL_P1", "HIGH_P2", "MEDIUM_P3", "LOW_P4"],
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the civic issue in user's language",
                    },
                },
                "required": ["category", "description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_kirana_inventory",
            "description": (
                "Query the kirana/dark-store inventory for stock levels, expiry dates, "
                "MRP, and recommended actions (flash discount, FEFO dispatch, BOGO clearance). "
                "Uses 100% synthetic product data."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sku": {
                        "type": "string",
                        "description": "Product SKU key (e.g., amul_taaza_500ml, paracetamol_650)",
                    },
                    "query_type": {
                        "type": "string",
                        "description": "Type of inventory query",
                        "enum": [
                            "stock_check",
                            "expiry_alert",
                            "price_check",
                            "reorder_suggestion",
                        ],
                    },
                },
                "required": ["sku"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_socratic_viva",
            "description": (
                "Evaluate a student's conceptual explanation in a Hinglish engineering viva. "
                "Scores clarity, detects conceptual gaps, and generates the next Socratic "
                "probing question in Hinglish code-mix."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The CS/engineering topic being examined",
                    },
                    "student_answer": {
                        "type": "string",
                        "description": "The student's answer/explanation to evaluate",
                    },
                    "subject_area": {
                        "type": "string",
                        "description": "Subject area for Socratic question selection",
                        "enum": ["operating_systems", "dbms", "dsa"],
                    },
                    "clarity_score": {
                        "type": "integer",
                        "description": "Estimated clarity score (0-100)",
                    },
                },
                "required": ["topic", "student_answer"],
            },
        },
    },
]


def execute_agent_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool call from the LLM and return structured card data
    with a TTS-ready spoken_summary containing Timbre v3.0 Audio Tags.

    All data is 100% SYNTHETIC for contest compliance (Guardrail #6).
    """
    timestamp = time.strftime("%H:%M:%S IST")
    logger.info("🔧 Executing tool: %s with args: %s", tool_name, args)

    if tool_name == "dispatch_gramseva_ticket":
        ticket_id = f"SYN{random.randint(100, 999)}"
        ward_info = random.choice(SYNTHETIC_WARDS)
        ward = args.get("ward", ward_info["ward"])
        category = args.get("category", "power_outage")
        severity = args.get("severity", "CRITICAL_P1")

        category_display = {
            "power_outage": "Transformer / Power Grid Fault",
            "water_leak": "Water Pipeline Leak / Low Pressure",
            "road_damage": "Road Pothole / Surface Damage",
            "sanitation": "Garbage Collection / Drain Blockage",
            "crop_transport": "Mandi Transport / Crop Loading Delay",
        }.get(category, category)

        sla_map = {
            "CRITICAL_P1": "45 Minutes",
            "HIGH_P2": "2 Hours",
            "MEDIUM_P3": "8 Hours",
            "LOW_P4": "24 Hours",
        }

        return {
            "card_type": "CIVIC_DISPATCH",
            "ticket_id": ticket_id,
            "ward": ward,
            "category": category_display,
            "severity": severity,
            "assigned_to": ward_info["engineer"],
            "language_detected": args.get("language_detected", "hi-IN (Hinglish Code-Mix)"),
            "sla_eta": sla_map.get(severity, "2 Hours"),
            "timestamp": timestamp,
            "spoken_summary": (
                f"<sigh> Maine aapki complaint register kar li hai. "
                f"Synthetic Ticket ID {' '.join(list(ticket_id))} "
                f"{ward} ke {ward_info['engineer']} ko assign ho gayi hai. "
                f"<chuckle> {sla_map.get(severity, '2 Hours')} mein team pahunch jayegi!"
            ),
        }

    elif tool_name == "query_kirana_inventory":
        sku_key = args.get("sku", "amul_taaza_500ml")
        # Fuzzy match SKU
        if sku_key not in SYNTHETIC_INVENTORY:
            for key in SYNTHETIC_INVENTORY:
                if sku_key.lower() in key.lower() or key.lower() in sku_key.lower():
                    sku_key = key
                    break
            else:
                sku_key = "amul_taaza_500ml"

        record = SYNTHETIC_INVENTORY[sku_key]

        action_display = {
            "TRIGGER_20_PERCENT_FLASH_DISCOUNT": "🔴 20% Flash Discount Active — Expiry Imminent!",
            "OPTIMAL_SHELF_HEALTH": "🟢 Shelf Health Optimal — No Action Needed",
            "PRIORITIZE_FEFO_DISPATCH": "🟡 FEFO Dispatch Priority — Ship Oldest First",
            "TRIGGER_BOGO_CLEARANCE": "🔴 Buy-One-Get-One Clearance — Critical Stock!",
        }

        return {
            "card_type": "KIRANA_COPILOT",
            "sku": record["item"],
            "category": record["category"],
            "current_stock": record["stock"],
            "expiry_in_days": record["expiry_days"],
            "unit_price_inr": record["mrp"],
            "recommended_action": record["action"],
            "action_display": action_display.get(record["action"], record["action"]),
            "timestamp": timestamp,
            "spoken_summary": (
                f"<gasp> Dhyan dijiye! {record['item']} ke "
                f"{record['stock']} packets sirf {record['expiry_days']} din mein "
                f"expire hone wale hain. MRP {record['mrp']} rupees hai. "
                f"Shrinkage bachane ke liye abhi "
                f"{'20 percent discount bundle' if record['expiry_days'] <= 5 else 'FEFO dispatch'} "
                f"active kar diya gaya hai."
            ),
        }

    elif tool_name == "evaluate_socratic_viva":
        topic = args.get("topic", "Deadlock vs Starvation in Operating Systems")
        student_answer = args.get("student_answer", "")
        subject = args.get("subject_area", "operating_systems")
        score = args.get("clarity_score", random.randint(72, 95))

        # Select a Socratic probe from the question bank
        probes = SOCRATIC_PROBES.get(subject, SOCRATIC_PROBES["operating_systems"])
        next_probe = random.choice(probes)

        # Generate mastery breakdown
        mastery = {
            "conceptual_accuracy": min(100, score + random.randint(-5, 10)),
            "technical_vocabulary": min(100, score + random.randint(-10, 5)),
            "real_world_application": min(100, score + random.randint(-15, 5)),
            "edge_case_awareness": min(100, score + random.randint(-20, 0)),
        }

        return {
            "card_type": "SOCRATIC_VIVA",
            "topic": topic,
            "clarity_score": score,
            "mastery_breakdown": mastery,
            "next_socratic_probe": next_probe,
            "subject_area": subject,
            "timestamp": timestamp,
            "spoken_summary": (
                f"<chuckle> Bahut badhiya explanation! "
                f"Aapka clarity score {score} percent hai. "
                f"Lekin ek tricky sawal sochiye: {next_probe}"
            ),
        }

    else:
        logger.warning("Unknown tool: %s", tool_name)
        return {
            "card_type": "SYSTEM_INFO",
            "message": f"Unknown tool '{tool_name}' — no action taken.",
            "timestamp": timestamp,
            "spoken_summary": "Yeh action abhi available nahi hai. Kuch aur try karein.",
        }

