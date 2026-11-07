"""
Inspect morph targets in avatar.glb
"""
import struct

with open("/Users/aarush/Desktop/Gnani Ai/bhashaswarm-3d/frontend/public/avatar/avatar.glb", "rb") as f:
    header = f.read(12)
    magic, version, length = struct.unpack("<4sII", header)
    print(f"GLB magic: {magic}, version: {version}, length: {length}")
    # Read first chunk
    chunk_len, chunk_type = struct.unpack("<I4s", f.read(8))
    print(f"First chunk: type={chunk_type}, length={chunk_len}")
    json_bytes = f.read(chunk_len)
    json_str = json_bytes.decode('utf-8', errors='ignore')
    import json
    data = json.loads(json_str)
    # Check meshes for target names
    if "meshes" in data:
        for m in data["meshes"]:
            if "extras" in m and "targetNames" in m["extras"]:
                print("Found morph target names:", m["extras"]["targetNames"][:15])
                break

