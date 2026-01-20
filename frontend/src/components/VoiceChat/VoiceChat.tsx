/**
 * VoiceChat Component (WebSocket Proxy Architecture)
 * 
 * Connects to backend WebSocket proxy which handles Azure VoiceLive connection.
 * Backend automatically persists transcripts to Zep memory.
 * 
 * This approach works with unified endpoints (services.ai.azure.com) which
 * don't support REST token endpoints.
 */

import { useState, useRef, useCallback, useEffect } from 'react';
import './VoiceChat.css';
import { getAccessToken } from '../../auth/authConfig';
import { normalizeApiBase } from '../../utils/url';
import { RTClientAvatar } from './RTClientAvatar';

interface VoiceMessage {
  id: string;
  type: 'user' | 'agent';
  text: string;
  agentId?: string;
  timestamp: Date;
}

interface Viseme {
  time_ms: number;
  viseme_id: number;
}

interface VoiceChatProps {
  agentId: string;
  sessionId?: string;
  onMessage?: (message: VoiceMessage) => void;
  onVisemes?: (visemes: Viseme[]) => void;
  onStatusChange?: (status: 'connecting' | 'connected' | 'error') => void;
  onAvatarVideo?: (url: string | undefined) => void;  // Callback for avatar video URL
  onAvatarStream?: (stream: MediaStream | null) => void; // Callback for WebRTC stream
  onSpeaking?: (speaking: boolean) => void;
  onAgentChange?: (agentId: string) => void; // Callback when agent switches dynamically
  disabled?: boolean;
  enableAvatar?: boolean;
}

export default function VoiceChat({
  agentId,
  sessionId: sessionIdProp,
  onMessage,
  onVisemes,
  onStatusChange,
  onAvatarVideo,
  onAvatarStream,
  onSpeaking,
  onAgentChange,
  disabled = false,
  enableAvatar = true
}: VoiceChatProps) {
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [userTranscription, setUserTranscription] = useState('');
  const [assistantTranscription, setAssistantTranscription] = useState('');
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'error'>('connecting');
  const [error, setError] = useState<string | null>(null);
  const [audioLevel, setAudioLevel] = useState(0);
  const [avatarVideoUrl, setAvatarVideoUrl] = useState<string | undefined>(undefined);

  const wsRef = useRef<WebSocket | null>(null);
  const videoWsRef = useRef<WebSocket | null>(null); // Fallback: Direct WebSocket to Azure (deprecated)
  const peerConnectionRef = useRef<RTCPeerConnection | null>(null); // WebRTC for avatar video
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const workletNodeRef = useRef<AudioWorkletNode | null>(null);
  const sourceNodeRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const playbackContextRef = useRef<AudioContext | null>(null);
  const playbackSourceRef = useRef<AudioBufferSourceNode | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const animationFrameRef = useRef<number>(0);
  const streamRef = useRef<MediaStream | null>(null);


  // Buffers for current turn
  const assistantTranscriptRef = useRef('');
  const userTranscriptRef = useRef('');

  // Track effective agent ID (prop + updates from backend)
  // We use STATE for rendering/effects and REF for callbacks
  const [activeAgentId, setActiveAgentId] = useState(agentId);
  const agentIdRef = useRef(agentId);

  // Sync prop changes to local state
  useEffect(() => {
    setActiveAgentId(agentId);
    agentIdRef.current = agentId;
  }, [agentId]);

  // Store callbacks
  const onMessageRef = useRef(onMessage);
  const onVisemesRef = useRef(onVisemes);
  const onStatusChangeRef = useRef(onStatusChange);
  const onAvatarVideoRef = useRef(onAvatarVideo);
  const onAvatarStreamRef = useRef(onAvatarStream);

  // Generate local session ID if not provided
  const [localSessionId] = useState(() => `voice-${Date.now()}`);
  const activeSessionId = sessionIdProp || localSessionId;

  // Audio Context & Worklet Refs
  const audioQueueRef = useRef<Float32Array[]>([]);
  const isPlayingRef = useRef(false);
  const nextStartTimeRef = useRef(0);
  const avatarClientRef = useRef<RTClientAvatar | null>(null);
  const avatarSpokenRef = useRef<string>(''); // track what we've already sent to Avatar TTS
  const avatarPendingRef = useRef<string>(''); // buffer incremental text before speaking
  const avatarLastSendMsRef = useRef<number>(0);

  // Initialize Avatar Client for Elena using RTClientAvatar (VoiceLive pattern)
  useEffect(() => {
    // Only initialize if agent is elena AND avatar is enabled
    if (activeAgentId === 'elena' && enableAvatar) {
      console.log('🤖 Initializing RTClientAvatar for Elena...');

      const client = new RTClientAvatar((stream: MediaStream) => {
        if (onAvatarStreamRef.current) {
          onAvatarStreamRef.current(stream);
        }
      });

      // Connect to VoiceLive Avatar service
      const connectAvatar = async () => {
        try {
          // Use westus2 regional endpoint for VoiceLive Avatar
          const endpoint = 'https://westus2.api.cognitive.microsoft.com/';

          // Fetch API key from backend (or use env var in dev)
          const baseUrl = normalizeApiBase(import.meta.env.VITE_API_URL as string | undefined, window.location.origin);
          const authToken = await getAccessToken().catch(() => null);

          let apiKey = '';
          try {
            const response = await fetch(`${baseUrl}/api/v1/voice/avatar/ice-credentials`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
              },
              body: JSON.stringify({ agent_id: 'elena', get_api_key: true })
            });
            if (response.ok) {
              const data = await response.json();
              apiKey = data.api_key || '';
            }
          } catch {
            console.warn('Could not fetch API key from backend, trying without');
          }

          await client.connect({
            endpoint,
            apiKey,
            model: 'gpt-realtime',
            voice: 'en-US-AvaMultilingualNeural',
            instructions: 'You are Elena, a helpful AI assistant.',
            avatarCharacter: 'lisa',
            avatarStyle: 'casual-sitting',
          });

          avatarClientRef.current = client;
          console.log('✅ RTClientAvatar connected successfully');
        } catch (e) {
          console.error('❌ Failed to connect RTClientAvatar:', e);
          avatarClientRef.current = null;
        }
      };

      connectAvatar();

      return () => {
        console.log('🔌 Disconnecting RTClientAvatar...');
        if (avatarClientRef.current) {
          avatarClientRef.current.disconnect();
          avatarClientRef.current = null;
        }
      };
    } else {
      // If switching AWAY from Elena, verify cleanup
      if (avatarClientRef.current) {
        avatarClientRef.current.disconnect();
        avatarClientRef.current = null;
      }
    }
  }, [activeAgentId, enableAvatar]); // Depend on activeAgentId and enableAvatar
  useEffect(() => {
    onMessageRef.current = onMessage;
    onVisemesRef.current = onVisemes;
    onStatusChangeRef.current = onStatusChange;
    onAvatarVideoRef.current = onAvatarVideo;
    onAvatarStreamRef.current = onAvatarStream;
  }, [onMessage, onVisemes, onStatusChange, onAvatarVideo, onAvatarStream]);

  const resolveApiUrl = useCallback(() => {
    const envApiUrl = import.meta.env.VITE_API_URL as string | undefined;
    const origin = window.location.origin;
    let apiUrl = normalizeApiBase(envApiUrl, origin);

    if (apiUrl.includes('localhost') && !/^(localhost|127\.0\.0\.1)$/.test(window.location.hostname)) {
      apiUrl = origin;
    }

    return apiUrl;
  }, []);

  const resolveWsUrl = useCallback((apiUrl: string) => {
    const envWsUrl = import.meta.env.VITE_WS_URL as string | undefined;
    const base = envWsUrl || apiUrl;
    return base.replace(/^https/, 'wss').replace(/^http/, 'ws');
  }, []);

  const isAuthRequired = useCallback(() => {
    const flag = import.meta.env.VITE_AUTH_REQUIRED as string | undefined;
    if (typeof flag === 'string') {
      return flag.toLowerCase() === 'true';
    }
    return import.meta.env.PROD;
  }, []);

  const checkBackendHealth = useCallback(async (apiUrl: string) => {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), 2500);

    try {
      const response = await fetch(`${apiUrl}/health`, {
        method: 'GET',
        cache: 'no-store',
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }

      return true;
    } catch (err) {
      console.warn('Voice backend unavailable:', err);
      setError('Voice service is unavailable. Please start the backend and try again.');
      setConnectionStatus('error');
      onStatusChangeRef.current?.('error');
      return false;
    } finally {
      window.clearTimeout(timeoutId);
    }
  }, []);

  // Notify parent when avatar video URL changes (legacy support)
  useEffect(() => {
    if (onAvatarVideoRef.current) {
      onAvatarVideoRef.current(avatarVideoUrl);
    }
  }, [avatarVideoUrl]);

  // Notify parent of speaking state changes
  useEffect(() => {
    onSpeaking?.(isSpeaking);
  }, [isSpeaking, onSpeaking]);

  // Audio Playback Context
  useEffect(() => {
    if (!playbackContextRef.current) {
      playbackContextRef.current = new AudioContext({ sampleRate: 24000 });
    }
    return () => {
      playbackContextRef.current?.close();
    };
  }, []);

  // Audio Processing Function (Recursive)
  const processAudioQueue = useCallback(function processQueue() {
    if (!playbackContextRef.current || audioQueueRef.current.length === 0) {
      isPlayingRef.current = false;
      playbackSourceRef.current = null;
      setIsSpeaking(false);
      return;
    }

    isPlayingRef.current = true;
    setIsSpeaking(true);
    const audioData = audioQueueRef.current.shift();
    if (!audioData) return;

    if (playbackContextRef.current.state === 'suspended') {
      try {
        playbackContextRef.current.resume();
      } catch (e) {
        console.warn("Failed to resume playback context:", e);
      }
    }

    const buffer = playbackContextRef.current.createBuffer(1, audioData.length, 24000);
    buffer.getChannelData(0).set(audioData);

    const source = playbackContextRef.current.createBufferSource();
    source.buffer = buffer;
    source.connect(playbackContextRef.current.destination);
    playbackSourceRef.current = source;

    const currentTime = playbackContextRef.current.currentTime;
    const startTime = Math.max(currentTime, nextStartTimeRef.current);

    source.start(startTime);
    nextStartTimeRef.current = startTime + buffer.duration;

    source.onended = () => {
      if (playbackSourceRef.current === source) {
        playbackSourceRef.current = null;
      }
      processQueue();
    };
  }, []);

  const interruptAssistant = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'cancel' }));
    }

    audioQueueRef.current = [];
    isPlayingRef.current = false;
    if (playbackSourceRef.current) {
      try {
        playbackSourceRef.current.stop();
      } catch (error) {
        console.warn('Failed to stop current playback source:', error);
      }
      playbackSourceRef.current = null;
    }
    if (playbackContextRef.current) {
      nextStartTimeRef.current = playbackContextRef.current.currentTime;
    }
    setIsSpeaking(false);
    setIsProcessing(false);
  }, []);

  // Enqueue Audio
  const enqueueAudio = useCallback((base64Audio: string) => {
    try {
      const binaryString = atob(base64Audio);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      const int16 = new Int16Array(bytes.buffer);
      const float32 = new Float32Array(int16.length);
      for (let i = 0; i < int16.length; i++) {
        float32[i] = int16[i] / 32768.0;
      }

      audioQueueRef.current.push(float32);

      if (!isPlayingRef.current) {
        if (playbackContextRef.current) {
          nextStartTimeRef.current = playbackContextRef.current.currentTime;
        }
        processAudioQueue();
      }
    } catch (e) {
      console.error('Audio decode error:', e);
    }
  }, [processAudioQueue]);

  // Main Connection Logic - WebSocket Proxy
  useEffect(() => {
    let mounted = true;

    const connectToBackend = async () => {
      try {
        setConnectionStatus('connecting');
        setError(null);

        // Get JWT token for authentication
        let token: string | null = null;
        try {
          token = await getAccessToken();
        } catch (error) {
          console.warn('Failed to get access token for voice WebSocket:', error);
          // Continue without token - backend will handle authentication
        }

        if (isAuthRequired() && !token) {
          // Don't block here - let the backend decide if auth is required
          // Backend has its own AUTH_REQUIRED setting and will close with code 1008 if needed
          console.warn('No auth token available for voice, attempting connection anyway (backend will validate)');
        }

        // Connect to backend WebSocket proxy endpoint
        const apiUrl = resolveApiUrl();

        // Preflight health check to avoid noisy WS errors when backend is down
        const healthy = await checkBackendHealth(apiUrl);
        if (!healthy) {
          return;
        }

        let wsUrl = resolveWsUrl(apiUrl) + `/api/v1/voice/voicelive/${activeSessionId}`;

        // Append token as query parameter if available
        if (token) {
          wsUrl += `?token=${encodeURIComponent(token)}`;
        } else if (isAuthRequired()) {
          console.warn('No access token available for voice WebSocket - connection may fail because auth is required');
        }

        const ws = new WebSocket(wsUrl);

        ws.onopen = () => {
          if (!mounted) return;
          setConnectionStatus('connected');
          onStatusChangeRef.current?.('connected');

          // Backend handles agent configuration automatically based on session
          // If we need to switch agent, send agent message
          if (agentId) {
            ws.send(JSON.stringify({
              type: 'agent',
              agent_id: agentId
            }));
          }
        };

        ws.onmessage = (event) => {
          if (!mounted) return;

          try {
            const data = JSON.parse(event.data);

            switch (data.type) {
              case 'audio':
                // Audio chunk from assistant
                if (data.data) {
                  // If Avatar is active (Elena) and avatar is enabled, we ALWAYS ignore backend audio.
                  // This allows the Avatar SDK to handle TTS fully and prevents "double audio" race conditions.
                  if (agentIdRef.current === 'elena' && enableAvatar) {
                    // Drop backend audio, Avatar SDK will generate it from text
                    // console.log('Dropping backend audio for Avatar');
                  } else {
                    enqueueAudio(data.data);
                    setIsSpeaking(true);
                  }
                }
                break;

              case 'transcription':
                // Transcript updates (user or assistant)
                if (data.speaker === 'user') {
                  if (data.status === 'complete') {
                    // Final user transcript
                    const finalText = data.text || '';
                    setUserTranscription(finalText);
                    userTranscriptRef.current = '';
                    if (finalText) {
                      onMessageRef.current?.({
                        id: `user-${Date.now()}`,
                        type: 'user',
                        text: finalText,
                        timestamp: new Date()
                      });
                    }
                  } else if (data.status === 'processing') {
                    // Partial user transcript
                    setUserTranscription(data.text || '');
                    userTranscriptRef.current = data.text || '';
                  } else if (data.status === 'listening') {
                    setIsProcessing(true);
                  }
                } else if (data.speaker === 'assistant') {
                  if (data.status === 'complete') {
                    // Final assistant transcript
                    const finalText = data.text || '';
                    setAssistantTranscription(finalText);
                    assistantTranscriptRef.current = '';
                    setIsProcessing(false);
                    if (finalText) {
                      onMessageRef.current?.({
                        id: `assistant-${Date.now()}`,
                        type: 'agent',
                        text: finalText,
                        agentId,
                        timestamp: new Date()
                      });
                    }
                  } else if (data.status === 'processing') {
                    // Partial assistant transcript
                    setAssistantTranscription(data.text || '');
                    assistantTranscriptRef.current = data.text || '';
                    setIsProcessing(false);

                  } else if (data.status === 'complete_phrase' || (data.status === 'complete' && !data.text)) {
                    // Handle phrase completion if backend supports it
                  }

                  // Trigger Avatar on COMPLETE (safer for POC)
                  if (agentIdRef.current === 'elena' && avatarClientRef.current?.isConnected && typeof data.text === 'string') {
                    const fullText = data.text;
                    const prev = avatarSpokenRef.current;

                    // Compute incremental delta (VoiceLive "processing" is typically "full so far").
                    let delta = '';
                    if (fullText.startsWith(prev)) {
                      delta = fullText.slice(prev.length);
                    } else if (fullText.length < prev.length) {
                      // New response / reset
                      avatarSpokenRef.current = '';
                      avatarPendingRef.current = '';
                      delta = fullText;
                    } else {
                      // Non-prefix mismatch; treat as full replace
                      avatarSpokenRef.current = '';
                      avatarPendingRef.current = '';
                      delta = fullText;
                    }

                    if (delta) {
                      avatarPendingRef.current += delta;
                      avatarSpokenRef.current = fullText;
                    }

                    const now = Date.now();
                    const pending = avatarPendingRef.current.trim();
                    const timeSinceLast = now - avatarLastSendMsRef.current;
                    const shouldFlush =
                      data.status === 'complete' ||
                      pending.length >= 40 ||
                      /[.!?]\s*$/.test(pending) ||
                      timeSinceLast >= 700;

                    if (shouldFlush && pending) {
                      avatarLastSendMsRef.current = now;
                      avatarPendingRef.current = '';
                      avatarClientRef.current.speak(pending).catch((e: any) => {
                        console.warn('Avatar speak failed, falling back to backend audio:', e);
                      });
                      setIsSpeaking(true);
                    }
                  }
                }
                break;

              case 'avatar_video':
                // Avatar video chunk from VoiceLive (streaming - not currently used)
                // Future: could assemble chunks into video blob
                if (data.data) {
                  setIsSpeaking(true);
                }
                break;

              case 'avatar_video_url':
                // Avatar video URL (final video)
                if (data.url) {
                  setAvatarVideoUrl(data.url);
                  setIsSpeaking(true);
                  console.log('Avatar video URL received:', data.url);
                }
                break;

              case 'agent_switched':
                // Agent was switched (backend confirms)
                console.log('Agent switched to:', data.agent_id);
                agentIdRef.current = data.agent_id; // Update local ref immediately
                setActiveAgentId(data.agent_id); // Update local state to trigger effects
                onAgentChange?.(data.agent_id); // Notify parent component

                // Clear avatar when switching agents
                setAvatarVideoUrl(undefined);
                setAvatarVideoUrl(undefined);
                if (onAvatarStreamRef.current) {
                  onAvatarStreamRef.current(null);
                }
                // Close existing video connection if any
                if (videoWsRef.current) {
                  videoWsRef.current.close();
                  videoWsRef.current = null;
                }
                break;

              case 'video_connection_ready':
                // Backend has prepared video connection
                // CRITICAL FIX: If 'video_connection' payload exists (token), it is meant for the Avatar Client SDK.
                // We MUST NOT trigger the legacy backend-proxy WebRTC flow (establishWebRTCVideoConnection)
                // regardless of what agentIdRef says (fixes race conditions).
                if (data.video_connection) {
                  console.log('ℹ️ Ignoring backend video_connection_ready for Avatar (SDK Token received)', data.video_connection.endpoint);
                  // The AvatarClient handles its own connection via fetchToken() or we could use this token.
                  // For now, we rely on AvatarClient's internal logic which is already running.
                } else if (agentIdRef.current === 'elena' || activeAgentId === 'elena') {
                  console.log('ℹ️ Ignoring backend video_connection_ready for Avatar (Agent is Elena)');
                } else {
                  // Only legacy agents without SDK support use this path
                  console.log(`🎥 Video connection ready for ${agentIdRef.current}, establishing legacy WebRTC connection...`);
                  establishWebRTCVideoConnection();
                }
                break;

              case 'avatar_sdp_answer':
              case 'avatar_answer':
                // Backend returns SDP answer for WebRTC avatar (both naming conventions supported)
                // If we are using AvatarClient, we should NOT be receiving this usually, unless it's a legacy path artifact.
                console.log('📥 Received SDP answer for avatar (Legacy Path)');
                if (agentIdRef.current !== 'elena') {
                  if (data.sdp) {
                    handleSdpAnswer(data.sdp);
                  }
                } else {
                  console.log('ℹ️ Ignoring legacy SDP answer for Elena');
                }
                break;

              case 'remote_ice_candidate':
                // Backend forwards remote ICE candidate
                console.log('🧊 Received remote ICE candidate');
                if (agentIdRef.current !== 'elena') {
                  if (data.candidate) {
                    handleRemoteIceCandidate(data.candidate);
                  }
                }
                break;

              case 'avatar_status':
                // Avatar status update (e.g., negotiating, connected)
                console.log('Avatar Status:', data.status, data.message);
                if (data.status === 'negotiating') {
                  // status is negotiating
                } else if (data.status === 'ready') {
                  setAvatarVideoUrl('webrtc://ready');
                }
                break;

              case 'error':
                console.error('VoiceLive Error:', data);
                setError(data.message || 'Unknown error');
                setConnectionStatus('error');
                onStatusChangeRef.current?.('error');
                break;

              default:
                console.log('Unknown message type:', data.type, data);
            }
          } catch (e) {
            console.error('Failed to parse WebSocket message:', e, event.data);
          }
        };

        ws.onerror = (e) => {
          console.error('Voice WebSocket error', e);
          if (mounted) {
            setError('Voice connection error. Check console for details.');
            setConnectionStatus('error');
            onStatusChangeRef.current?.('error');
          }
        };

        ws.onclose = (event) => {
          console.log('Voice WebSocket closed', event.code, event.reason);
          if (mounted) {
            setConnectionStatus('error');
            if (event.code === 1008) {
              const reason = event.reason || 'Invalid or missing token';
              console.error(`Voice WebSocket authentication failed: ${reason}`);
              setError(`Authentication failed: ${reason}. Please refresh and try again.`);
            } else if (event.code !== 1000) {
              // 1000 is normal closure, others are errors
              const reason = event.reason || 'Unknown reason';
              console.error(`Voice WebSocket closed with error: ${reason} (code: ${event.code})`);
              setError(`Connection closed: ${reason}`);
            }
            onStatusChangeRef.current?.('error');
          }
        };

        wsRef.current = ws;

      } catch (err: any) {
        if (!mounted) return;
        console.error('Connection failed:', err);
        setError(err.message || 'Failed to connect');
        setConnectionStatus('error');
        onStatusChangeRef.current?.('error');
      }
    };

    connectToBackend();

    return () => {
      mounted = false;
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
      if (videoWsRef.current) {
        videoWsRef.current.close();
        videoWsRef.current = null;
      }
    };
  }, [activeSessionId]);

  // NOTE: Old WebSocket-based establishVideoConnection removed
  // Using WebRTC-based establishWebRTCVideoConnection instead (see below)

  // NEW: Establish WebRTC video connection for avatar
  // This is the proper implementation using WebRTC instead of broken WebSocket
  const establishWebRTCVideoConnection = useCallback(async () => {
    console.log('🎥 Starting WebRTC avatar video connection...');

    try {
      // Close existing connections
      if (peerConnectionRef.current) {
        peerConnectionRef.current.close();
        peerConnectionRef.current = null;
      }

      // 1. Fetch ICE credentials from backend
      const apiUrl = normalizeApiBase(import.meta.env.VITE_API_URL as string | undefined, window.location.origin);
      console.log('📡 Fetching ICE credentials from backend...');

      const iceResponse = await fetch(`${apiUrl}/api/v1/voice/avatar/ice-credentials`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ agent_id: agentId }),
      });

      if (!iceResponse.ok) {
        const errorText = await iceResponse.text();
        console.error('❌ Failed to get ICE credentials:', iceResponse.status, errorText);
        return;
      }

      const iceConfig = await iceResponse.json();
      console.log('✅ ICE credentials received:', {
        urls: iceConfig.urls,
        username: iceConfig.username?.substring(0, 10) + '...',
        ttl: iceConfig.ttl,
      });

      // 2. Create WebRTC peer connection with ICE servers
      // CRITICAL: Force relay transport for Azure Avatar (required for NAT traversal)
      // See docs/architecture/azure-avatar-integration.md for details
      const peerConnection = new RTCPeerConnection({
        iceServers: [{
          urls: iceConfig.urls,
          username: iceConfig.username,
          credential: iceConfig.credential,
        }],
        // iceTransportPolicy: 'relay', // Relaxed: Allow all transport types (P2P + Relay) to improve connection success
      });
      peerConnectionRef.current = peerConnection;

      // 3. Set up track handlers for video/audio streams
      peerConnection.ontrack = (event) => {
        console.log('📹 WebRTC track received:', event.track.kind);

        if (event.track.kind === 'video') {
          const stream = event.streams[0];
          console.log('✅ Avatar video stream connected');
          setIsSpeaking(true);
          // setAvatarVideoUrl('webrtc://connected'); // Removed: connection handled via onAvatarStream

          // Pass stream to parent for rendering
          if (onAvatarStreamRef.current) {
            onAvatarStreamRef.current(stream);
          }
        }

        if (event.track.kind === 'audio') {
          const audioElement = document.createElement('audio');
          audioElement.id = 'avatar-audio-player';
          audioElement.srcObject = event.streams[0];
          audioElement.autoplay = true;
          console.log('✅ Avatar audio stream connected');
        }
      };

      // 4. ICE candidate handling
      peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
          console.log('🧊 ICE candidate:', event.candidate.type);
          if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({
              type: 'ice_candidate',
              candidate: event.candidate.toJSON(),
            }));
          }
        }
      };

      peerConnection.oniceconnectionstatechange = () => {
        console.log('🔗 ICE connection state:', peerConnection.iceConnectionState);
        if (peerConnection.iceConnectionState === 'connected') {
          console.log('✅ WebRTC avatar connected!');
        } else if (peerConnection.iceConnectionState === 'failed') {
          console.error('❌ WebRTC connection failed');
        }
      };

      // 5. Add transceivers to receive video/audio
      peerConnection.addTransceiver('video', { direction: 'recvonly' });
      peerConnection.addTransceiver('audio', { direction: 'recvonly' });

      // 6. Create offer
      const offer = await peerConnection.createOffer();
      await peerConnection.setLocalDescription(offer);
      console.log('📤 SDP offer created');

      // 7. Send offer to backend for avatar session negotiation
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          type: 'avatar_connect',
          sdp: offer.sdp,
          agent_id: agentId,
        }));
        console.log('📤 SDP offer sent to backend for avatar negotiation');
      } else {
        console.warn('⚠️ Main WebSocket not connected, cannot send SDP offer');
      }

    } catch (error) {
      console.error('❌ Failed to establish WebRTC video connection:', error);
    }
  }, [agentId]);

  // Handle SDP answer from backend (for WebRTC avatar)
  const handleSdpAnswer = useCallback(async (sdp: string) => {
    if (!peerConnectionRef.current) {
      console.warn('⚠️ No peer connection to apply SDP answer');
      return;
    }

    try {
      await peerConnectionRef.current.setRemoteDescription({
        type: 'answer',
        sdp: sdp,
      });
      console.log('✅ SDP answer applied to peer connection');
    } catch (error) {
      console.error('❌ Failed to apply SDP answer:', error);
    }
  }, []);

  // Handle remote ICE candidate from backend
  const handleRemoteIceCandidate = useCallback(async (candidate: RTCIceCandidateInit) => {
    if (!peerConnectionRef.current) {
      console.warn('⚠️ No peer connection to add ICE candidate');
      return;
    }

    try {
      await peerConnectionRef.current.addIceCandidate(new RTCIceCandidate(candidate));
      console.log('✅ Remote ICE candidate added');
    } catch (error) {
      console.error('❌ Failed to add ICE candidate:', error);
    }
  }, []);

  // Handle agent switching when agentId prop changes
  useEffect(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN && agentId) {
      wsRef.current.send(JSON.stringify({
        type: 'agent',
        agent_id: agentId
      }));
    }
  }, [agentId]);

  // Mic Logic
  const startListening = async () => {
    try {
      if (connectionStatus !== 'connected') return;

      if (isSpeaking || isProcessing) {
        interruptAssistant();
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: { channelCount: 1, sampleRate: 24000 }
      });
      streamRef.current = stream;

      audioContextRef.current = new AudioContext({ sampleRate: 24000 });
      const source = audioContextRef.current.createMediaStreamSource(stream);
      sourceNodeRef.current = source;
      analyserRef.current = audioContextRef.current.createAnalyser();
      source.connect(analyserRef.current);
      updateAudioLevel();

      const sendPcm16 = (pcm16: Int16Array) => {
        const bytes = new Uint8Array(pcm16.buffer);
        let binary = '';
        for (let i = 0; i < bytes.byteLength; i++) {
          binary += String.fromCharCode(bytes[i]);
        }
        const base64 = btoa(binary);

        if (wsRef.current?.readyState === WebSocket.OPEN) {
          wsRef.current.send(JSON.stringify({
            type: 'audio',
            data: base64
          }));
        }
      };

      if (audioContextRef.current.audioWorklet?.addModule) {
        try {
          const workletUrl = new URL('/worklets/pcm16-processor.js', window.location.origin);
          await audioContextRef.current.audioWorklet.addModule(workletUrl.toString());
          const workletNode = new AudioWorkletNode(audioContextRef.current, 'pcm16-processor');
          workletNode.port.onmessage = (event) => {
            const pcm16 = event.data as Int16Array;
            if (pcm16?.buffer) {
              sendPcm16(pcm16);
            }
          };
          source.connect(workletNode);
          workletNode.connect(audioContextRef.current.destination);
          workletNodeRef.current = workletNode;
        } catch (error) {
          console.warn('AudioWorklet failed, falling back to ScriptProcessorNode', error);
        }
      }

      if (!workletNodeRef.current) {
        const processor = audioContextRef.current.createScriptProcessor(4096, 1, 1);
        processor.onaudioprocess = (e) => {
          const input = e.inputBuffer.getChannelData(0);
          const pcm16 = new Int16Array(input.length);
          for (let i = 0; i < input.length; i++) {
            const s = Math.max(-1, Math.min(1, input[i]));
            pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
          }
          sendPcm16(pcm16);
        };

        source.connect(processor);
        processor.connect(audioContextRef.current.destination);
        processorRef.current = processor;
      }

      setIsListening(true);
    } catch (e) {
      console.error('Mic error:', e);
      setError('Mic access denied');
    }
  };

  const stopListening = () => {
    if (!isListening) return;

    // Backend handles VAD (Voice Activity Detection) automatically
    // No need to send commit/response.create - backend detects speech end
    // Just stop sending audio chunks

    workletNodeRef.current?.disconnect();
    workletNodeRef.current = null;
    processorRef.current?.disconnect();
    processorRef.current = null;
    sourceNodeRef.current?.disconnect();
    sourceNodeRef.current = null;
    audioContextRef.current?.close();
    audioContextRef.current = null;
    streamRef.current?.getTracks().forEach(t => t.stop());
    streamRef.current = null;

    cancelAnimationFrame(animationFrameRef.current);
    setAudioLevel(0);
    setIsListening(false);
  };

  const updateAudioLevel = () => {
    if (analyserRef.current) {
      const array = new Uint8Array(analyserRef.current.frequencyBinCount);
      analyserRef.current.getByteFrequencyData(array);
      const avg = array.reduce((a, b) => a + b) / array.length;
      setAudioLevel(avg / 255);
      animationFrameRef.current = requestAnimationFrame(updateAudioLevel);
    }
  };

  // Button Class Helper
  const getButtonClass = () => {
    if (disabled) return 'voice-button disabled';
    if (connectionStatus === 'connecting') return 'voice-button disabled';
    if (connectionStatus === 'error') return 'voice-button disabled';
    if (isListening) return 'voice-button listening';
    if (isProcessing) return 'voice-button processing';
    if (isSpeaking) return 'voice-button speaking';
    return 'voice-button';
  };

  return (
    <div className="voice-chat">
      <audio ref={audioRef} className="hidden-audio" />

      {/* Voice Button */}
      <div className="voice-button-container">
        <button
          className={getButtonClass()}
          onPointerDown={(e) => {
            if (e.pointerType === 'mouse' && e.button !== 0) return;
            (e.currentTarget as HTMLButtonElement).setPointerCapture?.(e.pointerId);
            interruptAssistant();
            startListening();
          }}
          onPointerUp={(e) => {
            (e.currentTarget as HTMLButtonElement).releasePointerCapture?.(e.pointerId);
            stopListening();
          }}
          onPointerLeave={stopListening}
          onPointerCancel={stopListening}
          disabled={disabled || isProcessing}
          title={isListening ? 'Release to send' : 'Hold to speak'}
        >
          <div
            className="voice-ring"
            style={{
              '--scale': 1 + audioLevel * 0.5,
              '--opacity': isListening ? 0.8 : 0
            } as React.CSSProperties}
          />

          <div className="voice-icon">
            {isListening && (
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
              </svg>
            )}
            {isProcessing && (
              <div className="processing-spinner" />
            )}
            {isSpeaking && (
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z" />
              </svg>
            )}
            {!isListening && !isProcessing && !isSpeaking && (
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
              </svg>
            )}
          </div>
        </button>

        <span className="voice-status">
          {connectionStatus === 'connecting' && 'Connecting to voice...'}
          {connectionStatus === 'error' && error?.includes('coming soon') && 'Voice integration pending'}
          {connectionStatus === 'error' && !error?.includes('coming soon') && 'Voice connection error'}
          {isListening && 'Listening...'}
          {isProcessing && 'Processing...'}
          {isSpeaking && `${agentId === 'marcus' ? 'Marcus' : 'Elena'} speaking...`}
          {!isListening && !isProcessing && !isSpeaking && connectionStatus === 'connected' && 'Hold to speak'}
        </span>
      </div>

      {/* Transcription Display */}
      {userTranscription && (
        <div className="transcription">
          <span className="transcription-label">You said:</span>
          <span className="transcription-text">{userTranscription}</span>
        </div>
      )}

      {assistantTranscription && (
        <div className="transcription">
          <span className="transcription-label">
            {agentId === 'marcus' ? 'Marcus said:' : 'Elena said:'}
          </span>
          <span className="transcription-text">{assistantTranscription}</span>
        </div>
      )}

      {/* Error/Info Display */}
      {error && (
        <div className={`voice-error ${error.includes('coming soon') ? 'voice-info' : ''}`}>
          {error}
        </div>
      )}
    </div>
  );
}

