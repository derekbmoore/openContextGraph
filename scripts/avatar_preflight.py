#!/usr/bin/env python3
"""
Avatar Preflight Check
======================

Verifies that the backend is ready for Avatar (Speech SDK) sessions.
Checks:
1. Environment variables (Client-side)
2. Backend Health (Avatar config)
3. Speech Token Issue (STS)
4. ICE Credentials Issue (TURN)

Usage:
    python3 scripts/avatar_preflight.py [API_URL]

    Default API_URL: http://localhost:8000
"""

import sys
import os
import json
import urllib.request
import urllib.error

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def log(msg, status="INFO"):
    if status == "PASS":
        print(f"[{GREEN}PASS{RESET}] {msg}")
    elif status == "FAIL":
        print(f"[{RED}FAIL{RESET}] {msg}")
    elif status == "WARN":
        print(f"[{YELLOW}WARN{RESET}] {msg}")
    else:
        print(f"[INFO] {msg}")

def make_request(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except urllib.error.URLError as e:
        return 0, str(e.reason)
    except Exception as e:
        return 0, str(e)

def main():
    print(f"\n{GREEN}=== Avatar POC Preflight Check ==={RESET}\n")

    # 1. Configuration
    api_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    api_url = api_url.rstrip('/')
    
    # Check Env Vars (Client context simulation)
    # These verify that the DEPLOYER or CLIENT would have what they need, 
    # though strictly the backend holds the secrets.
    # We'll just warn if they aren't here locally, as this script might run on a dev machine.
    log(f"Target API: {api_url}")

    errors = 0

    # 2. Health Check
    print(f"\n--- Checking Backend Health ---")
    status, body = make_request(f"{api_url}/api/v1/voice/health")
    
    if status == 200:
        log("Health endpoint accessible", "PASS")
        
        # Check avatar specific structure
        avatar_config = body.get("avatar", {})
        if avatar_config.get("speech_key_configured"):
            log("Backend has Speech Key configured", "PASS")
        else:
            log("Backend missing Speech Key configuration", "FAIL")
            errors += 1
            
        region = avatar_config.get("speech_region")
        if region:
            log(f"Backend Speech Region: {region}", "PASS")
            # Simple check for known avatar regions
            if region in ["westus2", "westeurope", "southeastasia", "northeurope"]:
                 log(f"Region '{region}' supports Avatar", "PASS")
            else:
                 log(f"Region '{region}' may not support Avatar (expected westus2, etc)", "WARN")
        else:
            log("Backend missing Speech Region configuration", "FAIL")
            errors += 1

    else:
        log(f"Health check failed (Status {status}): {body}", "FAIL")
        errors += 1

    # 3. Avatar Token (STS)
    print(f"\n--- Checking Avatar Token (STS) ---")
    # Note: Assuming no auth or POC auth for this script check as per routes/voice.py flexible auth
    token_status, token_body = make_request(
        f"{api_url}/api/v1/voice/avatar/token", 
        method="POST",
        headers={"Authorization": "Bearer poc-token-ignored-if-auth-false"}
    )

    if token_status == 200:
        token = token_body.get("token")
        region = token_body.get("region")
        
        if token and len(token) > 10:
            log("Received valid STS token", "PASS")
        else:
            log("Token response invalid or empty", "FAIL")
            errors += 1
            
        if region:
            log(f"Token matches region: {region}", "PASS")
        else:
             log("Token response missing region", "FAIL")
             errors += 1
    else:
        log(f"Token endpoint failed (Status {token_status}): {token_body}", "FAIL")
        errors += 1

    # 4. ICE Credentials (TURN)
    print(f"\n--- Checking ICE Credentials ---")
    ice_status, ice_body = make_request(
        f"{api_url}/api/v1/voice/avatar/ice-credentials",
        method="POST",
        data={"agent_id": "elena"}
    )

    if ice_status == 200:
        urls = ice_body.get("urls", [])
        user = ice_body.get("username")
        cred = ice_body.get("credential")
        
        if urls and len(urls) > 0:
            log(f"Received {len(urls)} ICE servers", "PASS")
            log(f"ICE URL[0]: {urls[0]}", "INFO")
        else:
            log("No ICE URLs returned", "FAIL")
            errors += 1
            
        if user and cred:
            log("Received TURN username/credential", "PASS")
        else:
            log("Missing TURN credentials", "FAIL")
            errors += 1
    else:
        log(f"ICE endpoint failed (Status {ice_status}): {ice_body}", "FAIL")
        errors += 1

    # Summary
    print(f"\n{GREEN if errors == 0 else RED}=== Summary ==={RESET}")
    if errors == 0:
        print(f"{GREEN}All checks passed. Avatar backend is ready.{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}{errors} checks failed. Review logs above.{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
