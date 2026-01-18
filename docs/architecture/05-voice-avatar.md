# Voice & Avatar System

## Components

- **Voice Input**: Speech-to-text
- **Voice Output**: Real-time TTS
- **Avatar Video**: WebRTC streaming

## Architecture

```
Frontend ←→ WebSocket ←→ VoiceLive ←→ TTS/STT
    ↓
 WebRTC ←→ Signaling ←→ Avatar
```

## Implementation

See: `backend/voice/`

> **Note:** For deep troubleshooting of WebRTC, ICE, and Green Screen issues, see the [Deep Research Report](../../docs/research/2026-01-08-avatar-webrtc-research.md).

## TODO

- [ ] Document self-hosted TTS options (Piper)
- [ ] Document self-hosted STT options (Whisper)
