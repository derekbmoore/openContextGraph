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

## TODO

- [ ] Document self-hosted TTS options (Piper)
- [ ] Document self-hosted STT options (Whisper)
