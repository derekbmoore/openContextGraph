# Avatar & Voice System: Deployment & Verification Guide

**Status:** Draft / POC Verified
**Component:** VoiceLive / WebRTC Avatar
**Context:** Deployment, Verification, and Configuration

This document serves as the **operational guide** for deploying, configuring, and verifying the **Chat Voice Avatar** system. It bridges the gap between the [Architecture Flow](../architecture/06-chat-voice-avatar-flow.md) and deployment reality.

---

## 1. System Overview

The **Avatar & Voice System** enables real-time multimodal interaction:

1. **Voice Interaction (Audio)**: Handled via **VoiceLive** (WebSocket Proxy) for low latency.
    * *Path:* Browser ↔ specific Backend Proxy (`/api/v1/voice/voicelive/{session_id}`) ↔ Azure VoiceLive (WebSocket).
2. **Avatar Visualization (Video)**: Handled via **Azure Speech SDK** (Direct Client-to-Azure).
    * *Path:* Browser (SDK) ↔ Azure Speech Service (Avatar Relay).
    * *Auth:* Backend issues secure STS token via `POST /api/v1/voice/avatar/token`.
    * *Signaling:* SDK handles WebRTC negotiation internally properly (bypassing the need for manual ICE relay).

This **Client-Side SDK** architecture solves the video transmission issues by establishing a direct, optimized connection for the heavy video stream, while the backend maintains control over audio transcription and memory persistence.

---

## 2. Configuration & Prerequisites

Success depends on 3 layers of configuration: **Azure Resources**, **Backend Environment**, and **Frontend Environment**.

### 2.1 Azure Resources

You must provision these resources in a supported region (Standard 2026/2025 Preview).

| Resource | Service | Region Constraint | Purpose |
| :--- | :--- | :--- | :--- |
| **VoiceLive** | Azure AI Services | `eastus2`, `swedencentral` | Orchestrates voice conversation (GPT-4o Realtime). |
| **Speech** | Azure Speech | `westus2`, `westeurope`, `southeastasia` | **CRITICAL for Avatar.** Must be in a region supporting Avatar Relay. |
| **Foundry** | Azure AI Foundry | Same as VoiceLive | Project hosting for agents. |

> [!IMPORTANT]
> **Avatar Region Mismatch:** A common failure mode is deploying Speech in `eastus` (standard) instead of `westus2` (avatar-enabled). If ICE credentials fail, check your Speech resource region.

### 2.2 Backend Configuration (`.env` / ACA Secrets)

Ensure these variables are set in your backend container environment:

```bash
# === VoiceLive (Audio) ===
AZURE_VOICELIVE_ENDPOINT="wss://{ai-services-resource-name}.services.ai.azure.com/voice-live/realtime?api-version=2024-10-01-preview&model=gpt-realtime"
# Optional overrides (defaults live in backend/core/config.py)
AZURE_VOICELIVE_API_VERSION="2024-10-01-preview"
AZURE_VOICELIVE_MODEL="gpt-realtime"
AZURE_VOICELIVE_PROJECT_NAME="{foundry-project-name}"  # Only for project-based unified endpoints
# Auth strategy: Service Principal (Entra) preferred over Key
AZURE_TENANT_ID="{tenant-id}"          # For Azure SDK (DefaultAzureCredential)
AZURE_CLIENT_ID="{client-id}"          # For Azure SDK (Managed Identity or SPN)
AZURE_CLIENT_SECRET="{client-secret}"  # For Azure SDK (SPN only)
# OR (Fallback):
AZURE_VOICELIVE_KEY="{key}"

# === Avatar (Video) ===
# Must be a standard Speech resource key, NOT a VoiceLive key
AZURE_SPEECH_KEY="{speech-key}"
AZURE_SPEECH_REGION="westus2"  # Must match resource region

# === Security ===
# Entra ID JWT validation (API auth)
AZURE_AD_TENANT_ID="{entra-tenant-id}"
AZURE_AD_CLIENT_ID="{entra-app-client-id}"
AUTH_REQUIRED="true" # Enforce JWT for WebSocket connections
CORS_ORIGINS="https://your-frontend-domain.com,http://localhost:5173"
```

### 2.3 Frontend Configuration (`.env`)

```bash
# API Base URL (adjust for production)
VITE_API_URL="https://your-backend-api.containerapps.io"
# WebSocket Base URL (wss://)
VITE_WS_URL="wss://your-backend-api.containerapps.io"
# Auth (Enables "Activate Avatar" button security)
VITE_AUTH_REQUIRED="true"
```

### 2.4 Deployment Readiness Checklist (Customer Environments)

Use this checklist before declaring the environment ready:

1. **Azure resource alignment**
    * VoiceLive resource in `eastus2` or `swedencentral` (Realtime-capable).
    * Speech resource in `westus2`, `westeurope`, or `southeastasia` (Avatar Relay).
    * Foundry project (if used) matches `AZURE_VOICELIVE_PROJECT_NAME`.
2. **Model availability**
    * `gpt-realtime` is deployed/available on the VoiceLive resource.
    * If using project-based unified endpoints, ensure the model is deployed within the project.
3. **Authentication posture**
    * **Production:** Prefer Managed Identity or Service Principal (Azure SDK env vars).
    * **POC/Staging:** API key is acceptable but should be scoped and rotated.
    * JWT validation enabled with `AUTH_REQUIRED=true` and Entra app IDs configured.
4. **Networking / firewall**
    * Browser egress allows UDP `3478` + `49152–65535`.
    * Backend allows outbound to `*.services.ai.azure.com` and `*.tts.speech.microsoft.com`.
5. **Backend validation logs**
    * Startup logs include “Voice Configuration Validation” with ✅ status (or warnings only).
    * No “Avatar Region Mismatch” errors from `VoiceConfigValidator`.

---

## 3. Verification Steps (POC & Deployment)

Use this checklist to verify the system post-deployment.

### Step 0: Preflight Validation Script (Automated)

**Goal:** Run the automated preflight check locally or in CI/CD to verify all endpoints (Health, Token, ICE).

1. **Run the script:**

   ```bash
   python3 scripts/avatar_preflight.py [BACKEND_API_URL]
   # Example: python3 scripts/avatar_preflight.py https://api.my-customer-env.com
   ```

2. **Output:**
   The script checks:
   * **Backend Health:** (Status 200, Avatar config present)
   * **Speech Token (STS):** (Status 200, Valid Token + Region)
   * **ICE Credentials:** (Status 200, Valid TURN config)

**Go/No-Go:** If any check fails, resolve before manual testing.

### Step 1: Manual Health Check (Recommended)

**Goal:** Verify VoiceLive + Avatar configuration in one call.

```bash
GET /api/v1/voice/health
```

* **Success:** `status: healthy` and `validation.errors` is empty.
* **Warnings only:** `status: healthy` with `validation.warnings` (audio-only mode may still work).
* **Failure:** `status: unhealthy` with actionable errors (fix before go-live).

### Step 1: Connectivity Check

**Goal:** Confirm backend can talk to Azure APIs.

1. **Hit the Status Endpoint:**

    ```bash
    GET /api/v1/voice/config/elena
    ```

    * **Success:** JSON 200 OK with `endpoint_configured: true`.
    * **Failure:** 500 Error -> Check `AZURE_VOICELIVE_ENDPOINT` variable.

### Step 2: STS Token Generation (Avatar Auth)

**Goal:** Confirm backend can issue secure tokens for the Speech SDK.

1. **Test Token Endpoint:**

    ```bash
    POST /api/v1/voice/avatar/token
    ```

    * **Success:** JSON 200 OK with `token` and `region`.
    * **Failure:** 500 Error -> Check `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` in backend secrets.

### Step 3: "Activate Avatar" Flow (End-to-End)

**Goal:** Confirm Frontend <-> Backend <-> Azure relay.

1. Open the Chat UI.
2. Click **"Activate Avatar"** (previously "Activate Voice").
3. **Observation:**
    * **Phase 1 (Connecting):** Overlay appears. Spinner/Loader.
    * **Phase 2 (Audio):** "Mic" icon appears. Speak "Hello".
    * **Phase 3 (Video):** Avatar video should appear within 3-5 seconds.
    * **Phase 4 (Legacy Fallback):** If video fails, you will see a static image but hear audio.

---

## 4. Refinements & Best Practices

### 4.1 UI "Glow" & Visual Polish

* **Static State:** We reduced the cyan "glow" on the static avatar circle to prevent it from looking glitchy behind UI panels.
* **Active State:** The glow now pulses *only* when the avatar is speaking (VAD-triggered).

### 4.2 Network & Firewalls (Corporate Deployments)

* **WebRTC Ports:** Ensure usage of UDP ports `3478` (STUN/TURN) and the ephemeral range `49152–65535` is allowed for outbound traffic from client browsers.
* **WebSocket:** Ensure `wss://` (TCP 443) is allowed to your backend domain.

### 4.3 Chat-Only Mode

We introduced a **"Chat Only"** button in the overlay.

* **Use Case:** User started voice but changed their mind or is in a noisy environment.
* **Behavior:** Immediately closes WebRTC/WebSocket and returns to the text chat interface without error.

---

## 5. Troubleshooting Cheat Sheet

| Symptom | Probable Cause | Fix |
| :--- | :--- | :--- |
| **"Activate Avatar" button missing** | `voiceEnabled: false` in Agent config | Check `frontend/src/types.ts` (AGENTS definition) or backend agent configuration in `backend/core/config.py`. |
| **Audio works, Video is black** | Region mismatch or Token failure | 1. Check `AZURE_SPEECH_REGION` is `westus2` (or supported). <br> 2. Check Console for "AvatarClient" errors. <br> 3. Verify `POST /api/v1/voice/avatar/token` is returning 200 OK. |
| **"Connection Error" immediately** | 401 Unauthorized / CORS | 1. Check `CORS_ORIGINS` in backend (and `ALLOWED_ORIGINS`). <br> 2. Confirm `AZURE_AD_TENANT_ID` + `AZURE_AD_CLIENT_ID` match the Entra app. <br> 3. Ensure `VITE_API_URL` uses `https://` (not http) for prod. |
| **"Glowing" artifact behind panel** | Old CSS | **Fixed in latest version**. Ensure you have the latest `ChatPanel.css` with reduced `box-shadow`. |
| **Avatar sync is lip-flapping only** | WebRTC failed, fallback active | System fell back to "Viseme-based animation" (CSS) because the video stream didn't arrive. Check Step 2 (Token/ICE). |
| **Double Audio / Echo** | Backend Audio Leak | The Avatar SDK generates its own audio. Ensure `VoiceChat.tsx` logic is suppressing backend audio chunks when `agentId === 'elena'`. |
| **Component Crash (Blank Screen)** | SDK Version Mismatch / Missing Features | **Fixed.** `AvatarClient.ts` now uses robust `try/catch` and existence checks for experimental SDK features (`AvatarVideoFormat`), falling back to safe defaults if missing. |
| **Voice WebSocket Closed 1005 (Disconnect)** | Race Condition (Legacy vs Avatar) | **Fixed.** Older WebRTC logic in `VoiceChat.tsx` was conflicting with the Avatar SDK connection. We now explicitly ignore backend `video_connection_ready` signals when `elena` is active. |

---

## 6. POC "Working Document" Notes

For the **Proof of Concept (POC)**, stick to this "Golden Path":

1. **Agent:** Use `elena` (default).
2. **Voice:** Use `en-US-Ava:DragonHDLatestNeural` (default VoiceLive voice, most expressive).
3. **Region:** `westus2` (safest bet for Video).
4. **Client:** Chrome or Edge (Safari WebRTC implementation can be finicky with strict corporate firewalls).

*End of Guide.*
