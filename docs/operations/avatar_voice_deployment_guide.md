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
2. **Avatar Visualization (Video)**: Handled via **Azure Speech Avatar Relay** (WebRTC).
    * *Path:* Browser ↔ Azure Speech Relay (Direct WebRTC).
    * *Signaling:* Backend provides ICE/TURN credentials via `/api/v1/voice/avatar/ice-credentials`.

This "Split Path" architecture ensures audio persistence (via backend for memory) while offering low-latency video (direct WebRTC).

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
AZURE_VOICELIVE_ENDPOINT="wss://{name}.services.ai.azure.com/voice-live/realtime?api-version=2025-10-01&model=gpt-realtime"
# Auth strategy: Service Principal (Entra) preferred over Key
AZURE_TENANT_ID="{tenant-id}"
AZURE_CLIENT_ID="{client-id}"
AZURE_CLIENT_SECRET="{client-secret}"
# OR (Fallback):
AZURE_VOICELIVE_KEY="{key}"

# === Avatar (Video) ===
# Must be a standard Speech resource key, NOT a VoiceLive key
AZURE_SPEECH_KEY="{speech-key}"
AZURE_SPEECH_REGION="westus2"  # Must match resource region

# === Security ===
AUTH_REQUIRED="true" # Enforce JWT for WebSocket connections
ALLOWED_ORIGINS="https://your-frontend-domain.com,http://localhost:5173"
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

---

## 3. Verification Steps (POC & Deployment)

Use this checklist to verify the system post-deployment.

### Step 1: Connectivity Check

**Goal:** Confirm backend can talk to Azure APIs.

1. **Hit the Status Endpoint:**

    ```bash
    GET /api/v1/voice/config/elena
    ```

    * **Success:** JSON 200 OK with `endpoint_configured: true`.
    * **Failure:** 500 Error -> Check `AZURE_VOICELIVE_ENDPOINT` variable.

### Step 2: ICE Credentials (Avatar Signaling)

**Goal:** Confirm backend can generate WebRTC tokens.

1. **Test Credential Generation:**

    ```bash
    POST /api/v1/voice/avatar/ice-credentials
    body: { "agent_id": "elena" }
    ```

    * **Success:** Returns JSON with `urls` (TURN servers), `username`, and `credential`.
    * **Failure:** 500 Error -> Check `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION`.
    * **Failure (401):** Check JWT token validity or `AUTH_REQUIRED` settings.

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
| **"Activate Avatar" button missing** | `voiceEnabled: false` in Agent config | Check `Constants.ts` in frontend or Agent definition in backend. |
| **Audio works, Video is black** | Region mismatch or ICE failure | 1. Check `AZURE_SPEECH_REGION` is `westus2` (or supported). <br> 2. Check Browser Console for "ICE connection failed". |
| **"Connection Error" immediately** | 401 Unauthorized / CORS | 1. Check `ALLOWED_ORIGINS` in backend. <br> 2. Ensure `VITE_API_URL` uses `https://` (not http) for prod. |
| **"Glowing" artifact behind panel** | Old CSS | **Fixed in v0.1.2**. Ensure you have the latest `ChatPanel.css` with reduced `box-shadow`. |
| **Avatar sync is lip-flapping only** | WebRTC failed, fallback active | System fell back to "Viseme-based animation" (CSS) because the video stream didn't arrive. Check Step 2 (ICE). |

---

## 6. POC "Working Document" Notes

For the **Proof of Concept (POC)**, stick to this "Golden Path":

1. **Agent:** Use `elena` (default).
2. **Voice:** Use `en-US-AvaMultilingualNeural` (most expressive).
3. **Region:** `westus2` (safest bet for Video).
4. **Client:** Chrome or Edge (Safari WebRTC implementation can be finicky with strict corporate firewalls).

*End of Guide.*
