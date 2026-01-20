import { useState, useRef, useEffect, useCallback } from 'react';
import type { Agent } from '../../types';
import VoiceChat from '../VoiceChat/VoiceChat';
import AvatarDisplay from '../AvatarDisplay/AvatarDisplay';
import './AvatarCenterPanel.css';

interface AvatarCenterPanelProps {
    agent: Agent;
    sessionId: string;
}

export function AvatarCenterPanel({ agent, sessionId }: AvatarCenterPanelProps) {
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [avatarStream, setAvatarStream] = useState<MediaStream | null>(null);
    const [voiceReady, setVoiceReady] = useState(false);
    const [status, setStatus] = useState<'connecting' | 'connected' | 'error'>('connecting');
    const [error, setError] = useState<string | null>(null);

    // Video element ref for WebRTC stream
    const videoRef = useRef<HTMLVideoElement>(null);

    // Attach WebRTC stream to video element
    useEffect(() => {
        if (videoRef.current && avatarStream) {
            console.log('📹 Attaching avatar stream to video element in Center Panel');
            videoRef.current.srcObject = avatarStream;
            videoRef.current.play().catch(e => console.warn('Video autoplay blocked:', e));
        }
    }, [avatarStream]);

    const handleAvatarStream = useCallback((stream: MediaStream | null) => {
        setAvatarStream(stream);
    }, []);

    const handleStatusChange = useCallback((newStatus: 'connecting' | 'connected' | 'error') => {
        setStatus(newStatus);
        if (newStatus === 'error') {
            setError('Connection failed.');
        } else {
            setError(null);
        }
    }, []);

    // If agent is NOT Elena, we might want to show something else or just standard avatar logic.
    // Spec says "Elena on the page", so we assume Elena behavior is priority.

    return (
        <div className="avatar-center-panel">
            <div className={`avatar-stage ${isSpeaking ? 'speaking' : ''}`}>
                {/* 
                  Requirement: "Only Avatar". "No Fallback".
                  However, we need a button to START the connection.
                */}

                {avatarStream ? (
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted={false} // Audio comes from VoiceChat? No, VoiceChat handles audio usually? 
                        // Actually VoiceChat.tsx handles audio playback on its own usually via Web Audio API or PeerConnection audio track.
                        // If PeerConnection has audio track, we need to let the video element play it?
                        // AvatarClient sets up audio transceiver. 
                        // Let's ensure muted is false if we expect audio from the stream.
                        // But VoiceChat.tsx often handles audio manually? 
                        // Let's stick to previous patterns: `muted={false}` on video element if stream carries audio.
                        className="avatar-video-element"
                    />
                ) : (
                    <div className="avatar-placeholder">
                        <AvatarDisplay
                            agentId={agent.id as any}
                            isSpeaking={isSpeaking}
                            size="lg"
                            showName={false}
                        // We don't verify fallback here, but we need something before connection starts
                        />

                        {!voiceReady && (
                            <button
                                className="activate-avatar-btn"
                                onClick={() => setVoiceReady(true)}
                            >
                                Connect Avatar
                            </button>
                        )}

                        {voiceReady && status === 'connecting' && (
                            <div className="connecting-spinner">Connecting...</div>
                        )}
                    </div>
                )}
            </div>

            {/* Error Message */}
            {error && <div className="avatar-error">{error}</div>}

            {/* Hidden VoiceChat Controller */}
            {voiceReady && (
                <VoiceChat
                    agentId={agent.id}
                    sessionId={sessionId}
                    onStatusChange={handleStatusChange}
                    onAvatarStream={handleAvatarStream}
                    onSpeaking={setIsSpeaking}
                    enableAvatar={true} // Strictly Enable Avatar Mode
                // We don't strictly need message handling here if ChatPanel handles chat history via API/Zep
                // BUT, VoiceChat emits 'onMessage' for live transcripts. 
                // If we want transcripts to appear in ChatPanel instantly, we need a way to pass them.
                // For now, let's assume ChatPanel polls or VoiceChat updates zep and ChatPanel sees it? 
                // Actually, ChatPanel usually listens to Websocket? 
                // VoiceChat.tsx IS the websocket connection. 
                // Refactor Note: ChatPanel MIGHT need to know about these messages.
                // Implementation Plan Step 1 said: "Lift VoiceChat state... or they just share session ID".
                // The user prompt didn't strictly ask for real-time transcript streaming to the right panel, 
                // but it's a good UX. 
                // For this iteration (Focus on Layout), we will decouple them. 
                // ChatPanel refreshes on user action or we might add a polling/event mechanism later.
                // Or we Keep it simple: VoiceChat handles the Voice/Video. ChatPanel handles text.
                />
            )}

            <div className="avatar-controls">
                {/* Optional Mute/Disconnect controls could go here */}
            </div>
        </div>
    );
}
