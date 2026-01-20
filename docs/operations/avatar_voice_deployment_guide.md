# Avatar & Voice System: Deployment & Verification Guide

**Status:** Live / RT-Client Integration
**Component:** VoiceLive / WebRTC Avatar
**Context:** Deployment, Verification, and Configuration

This document serves as the **operational guide** for deploying, configuring, and verifying the **Chat Voice Avatar** system. It reflects the architecture using **Microsoft's `rt-client`** for direct VoiceLive connectivity.

---

## 1. System Overview

The **Avatar & Voice System** enables real-time multimodal interaction through two distinct modes:

### Mode A: Avatar (Video + Audio) - **"Elena"**

* **Architecture:** Direct Client-to-Azure (Bypasses Backend Proxy).
* **Technology:** `rt-client` (Azure AI Realtime Audio SDK).
* **Path:** Browser `RTClient` ↔ Azure VoiceLive (WebSocket/WebRTC).
* **Auth:**
    1. Frontend requests credentials from Backend (`POST /api/v1/voice/avatar/ice-credentials`).
    2. Backend returns **ICE Servers** (for NAT traversal) and **Speech API Key** (securely scoped).
    3. Frontend establishes direct connection to Azure using these credentials.
* **Benefits:** Lowest possible latency for video syncing; uses Azure's native WebRTC signaling.

### Mode B: Voice Only (Audio)

* **Architecture:** WebSocket Proxy.
* **Technology:** FastApi WebSocket Relay.
* **Path:** Browser ↔ Backend Proxy (`/api/v1/voice/voicelive/{session_id}`) ↔ Azure VoiceLive.
* **Auth:** JWT (Entra ID) between Browser and Backend; Managed Identity between Backend and Azure.

---

## 2. Configuration & Prerequisites

Success depends on 3 layers of configuration: **Azure Resources**, **Backend Environment**, and **Frontend Environment**.

### 2.1 Azure Resources

You must provision these resources in a supported region.

| Resource | Service | Region Constraint | Purpose |
| :--- | :--- | :--- | :--- |
| **VoiceLive** | Azure AI Services | `eastus2`, `swedencentral` | **Audio-only** backend proxy connection. |
| **Speech** | Azure Speech | `westus2` | **CRITICAL for Avatar.** Must be in `westus2` for Avatar Video Relay. |

> [!IMPORTANT]
> **Avatar Region:** The simple `rt-client` implementation for avatars requires the **West US 2** endpoint (`https://westus2.api.cognitive.microsoft.com/`) to successfully negotiate WebRTC video.

### 2.2 Backend Configuration (`.env` / ACA Secrets)

Ensure these variables are set in your backend container environment:

```bash
# === VoiceLive (Audio Proxy) ===
AZURE_VOICELIVE_ENDPOINT="wss://{ai-resource}.services.ai.azure.com/voice-live/realtime?..."

# === Avatar (Video & Direct Client Auth) ===
# CRITICAL: This key is returned to the frontend for direct connection
AZURE_SPEECH_KEY="{speech-resource-key}"
AZURE_SPEECH_REGION="westus2"
```

### 2.3 Frontend Configuration (`.env`)

```bash
# API Base URL
VITE_API_URL="https://your-backend-api.containerapps.io"
```

---

## 3. Deployment Checklist

1. **Backend Update:**
    * Ensure `backend/api/routes/voice.py` has the **ICE Credentials Fix** (returns `api_key`).
    * Deploy backend container.

2. **Frontend Update:**
    * Ensure `VoiceChat.tsx` uses `RTClientAvatar`.
    * Deploy frontend (SWA).

3. **Firewall / Network:**
    * **UDP Ports:** Allow `3478` (STUN/TURN) and `49152–65535` (Media) outbound.
    * **Domains:** Allow `*.cognitive.microsoft.com` and `*.services.ai.azure.com`.

---

## 4. Verification Steps

### Step 1: Preflight (Backend Credentials)

Verify the backend is serving the correct credentials.

```bash
# Request ICE credentials + API Key
curl -X POST "https://api.ctxeco.com/api/v1/voice/avatar/ice-credentials" \
     -H "Content-Type: application/json" \
     -d '{"agent_id": "elena", "get_api_key": true}'
```

* **Success:** JSON response includes `Urls` (ICE servers) AND `api_key` (string).
* **Failure:** Missing `api_key` means backend code is outdated or `AZURE_SPEECH_KEY` env var is missing.

### Step 2: "Connect Avatar" Flow

1. Open Chat UI (`/`).
2. Click **"Connect Avatar"**.
3. **Open Console (F12):**
    * Look for: `RTClientAvatar: Connected successfully`.
    * Look for: `RTClientAvatar: WebRTC connected!`.
4. **Verify Video:** The static placeholder should disappear, replaced by the live video stream.

---

## 5. Troubleshooting Cheat Sheet

| Symptom | Probable Cause | Fix |
| :--- | :--- | :--- |
| **"HTTP Authentication failed"** | Backend didn't return API Key | 1. Check if backend is deployed with `get_avatar_ice_credentials` fix. <br> 2. Check `AZURE_SPEECH_KEY` in backend secrets. |
| **Video is black / Loading forever** | WebRTC Stalled | 1. Check Console for `RTClientAvatar: WebRTC connected!`. <br> 2. If missing, check UDP port blocking (Firewall). <br> 3. Verify Region is `westus2`. |
| **"Refused to connect"** | CORS | Check `ALLOW_ORIGINS` in backend config. |
| **Audio works, no mouth movement** | Video track missing | Verify `addTransceiver('video', { direction: 'sendrecv' })` is set (Done in `RTClientAvatar.ts`). |

---

## 6. Architecture Notes (`rt-client`)

We moved from the hybrid "AvatarSynthesizer" approach to the **VoiceLive Sample** architecture:

* **Logic:** `RTClientAvatar.ts`
* **Signaling:** Uses `RTClient.connectAvatar()` to exchange SDP directly with Azure.
* **Protocol:** This implementation uses the VoiceLive `2026-01-01-preview` API which handles both GPT-4o Realtime audio and Avatar video in a single session.
