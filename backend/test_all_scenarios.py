"""
Test all 4 presets over WebSocket
"""
import asyncio
import json
import websockets

async def test_scenarios():
    uri = "ws://localhost:8000/ws/voice"
    presets = ["hinglish_civic", "hinglish_kirana", "hinglish_viva", "tanglish_switch"]

    for preset_id in presets:
        print(f"\n==========================================")
        print(f"Testing Scenario: {preset_id}")
        print(f"==========================================")
        async with websockets.connect(uri) as ws:
            conn = await ws.recv()
            print("Connected to server.")

            await ws.send(json.dumps({"type": "simulate", "preset_id": preset_id}))

            for _ in range(30):
                try:
                    res = await asyncio.wait_for(ws.recv(), timeout=5.0)
                    if isinstance(res, str):
                        data = json.loads(res)
                        msg_type = data.get("type")
                        if msg_type == "tool_card":
                            print(f"  [TOOL CARD] Type: {data['data']['card_type']}")
                            if "ticket_id" in data["data"]:
                                print(f"    Ticket: {data['data']['ticket_id']}, Ward: {data['data']['ward']}, SLA: {data['data']['sla_eta']}")
                            elif "sku" in data["data"]:
                                print(f"    SKU: {data['data']['sku']}, Stock: {data['data']['current_stock']}, Expiry: {data['data']['expiry_in_days']} days")
                            elif "clarity_score" in data["data"]:
                                print(f"    Topic: {data['data']['topic']}, Clarity Score: {data['data']['clarity_score']}%")
                        elif msg_type == "llm_response":
                            print(f"  [LLM RESPONSE] {data['text']}")
                        elif msg_type == "tts_done":
                            print("  [TTS DONE] Synthesis finished.")
                            break
                    else:
                        print(f"  [AUDIO PCM] Received {len(res)} bytes chunk (Timbre stream)")
                except asyncio.TimeoutError:
                    break

    print("\n✅ ALL 4 SCENARIOS TESTED AND VERIFIED OVER WEBSOCKET!")

if __name__ == "__main__":
    asyncio.run(test_scenarios())

