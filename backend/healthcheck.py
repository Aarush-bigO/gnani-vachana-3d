#!/usr/bin/env python3
"""
Standalone zero-dependency healthcheck probe for Docker and Kubernetes liveness checks.
Pings the FastAPI health/status endpoint or verifies socket availability.
"""
import sys
import urllib.request
import os

PORT = int(os.environ.get("PORT", 8000))
URL = f"http://127.0.0.1:{PORT}/"

try:
    req = urllib.request.Request(URL, headers={"User-Agent": "HealthcheckProbe/1.0"})
    with urllib.request.urlopen(req, timeout=3) as resp:
        if resp.status == 200:
            sys.exit(0)
        else:
            sys.exit(1)
except Exception:
    sys.exit(1)
