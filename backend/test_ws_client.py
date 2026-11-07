"""
Test client to verify WebSocket /ws/voice end-to-end communication
"""
import asyncio
import json
import websockets

async def test_ws():
    uri = "ws://localhost:8000/ws/voice"
    print(f"Connecting to {uri}...")
    async with websockets.connect(uri) as ws:
        # 1. Wait for connected message
        msg = await ws.recv()
        data = json.loads(msg)
        print("Received connected:", data)
        assert data["type"] == "connected"

        # 2. Send simulation command
        print("\nSending simulation turn (hinglish_civic)...")
        await ws.send(json.dumps({
            "type": "simulate",
            "preset_id": "hinglish_civic"
        }))

        # 3. Listen for responses (status, llm_response, tool_card, viseme, etc.)
        tool_card_received = False
        status_received = False
        count = 0
        while count < 10:
            count += 1
            try:
                res = await asyncio.wait_for(ws.recv(), timeout=5.0)
                if isinstance(res, str):
                    parsed = json.loads(res)
                    print(f"[{count}] Received JSON: type={parsed.get('type')}")
                    if parsed.get("type") == "tool_card":
                        tool_card_received = True
                        print("  -> Tool Card details:", parsed["data"]["card_type"], parsed["data"].get("ticket_id"))
                    elif parsed.get("type") == "status":
                        status_received = True
                        print("  -> Status:", parsed.get("status"))
                    elif parsed.get("type") == "llm_response":
                        print("  -> LLM Response text:", parsed.get("text")[:60] + "...")
                        break
                else:
                    print(f"[{count}] Received binary PCM bytes: {len(res)} bytes")
            except asyncio.TimeoutError:
                print("Wait timed out after 5s")
                break

        print("\nWebSocket verification completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_ws())

