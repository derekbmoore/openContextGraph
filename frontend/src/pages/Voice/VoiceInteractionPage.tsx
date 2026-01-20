import { useState, useCallback } from 'react';
import './VoiceInteractionPage.css';
import VoiceChat from '../../components/VoiceChat/VoiceChat';
import type { AgentId } from '../../types';

interface VoiceInteractionPageProps {
  activeAgent: AgentId;
  sessionId: string;
}

/**
 * Mobile-First Voice Interaction Page (Voice Only)
 * 
 * Optimized for audio-only interaction.
 */
export function VoiceInteractionPage({ activeAgent, sessionId }: VoiceInteractionPageProps) {
  const [status, setStatus] = useState<'connecting' | 'connected' | 'error'>('connecting');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [voiceReady, setVoiceReady] = useState(false);


  // Handle status changes
  const handleStatusChange = useCallback((newStatus: 'connecting' | 'connected' | 'error') => {
    setStatus(newStatus);
    if (newStatus === 'error') {
      setError('Voice connection failed. Check your network and try again.');
    } else {
      setError(null);
    }
  }, []);

  const agentName = activeAgent === 'elena' ? 'Dr. Elena Vasquez'
    : activeAgent === 'marcus' ? 'Marcus Chen'
      : 'Sage Meridian';

  const agentRole = activeAgent === 'elena' ? 'Business Analyst'
    : activeAgent === 'marcus' ? 'Project Manager'
      : 'Storyteller';

  return (
    <div className="voice-page">
      {/* Main Voice Interface */}
      <section className="voice-controls-container">
        <div className="agent-voice-profile">
          {/* Simple static avatar or icon for Voice Mode */}
          <div className="voice-avatar-circle">
            <div className={`sending-ring ${isSpeaking ? 'active' : ''}`} />
            <img src={`https://raw.githubusercontent.com/zimaxnet/assets/main/avatars/${activeAgent}.png`} alt={activeAgent} className="static-avatar-img" />
          </div>

          <div className="agent-info">
            <h2>{agentName}</h2>
            <p className="role">{agentRole}</p>

            <div className="connection-status">
              <span className={`status-dot ${isSpeaking ? 'speaking' :
                !voiceReady ? 'error' :
                  status === 'connected' ? 'connected' :
                    status === 'connecting' ? 'connecting' : 'error'
                }`} />
              <span>
                {!voiceReady ? 'Inactive' :
                  isSpeaking ? 'Speaking...' :
                    status === 'connected' ? 'Ready' :
                      status === 'connecting' ? 'Connecting...' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="controls-wrapper">
          {error && (
            <div className="error-banner">
              <p>{error}</p>
              <button onClick={() => {
                setError(null);
                setStatus('connecting');
              }}>
                Retry Connection
              </button>
            </div>
          )}

          {!voiceReady ? (
            <div className="voice-activate">
              <button
                className="voice-activate-btn"
                onClick={() => {
                  setVoiceReady(true);
                  setStatus('connecting');
                  setError(null);
                }}
              >
                Start Voice Session
              </button>
            </div>
          ) : (
            <VoiceChat
              agentId={activeAgent}
              sessionId={sessionId}
              disabled={status !== 'connected'}
              onStatusChange={handleStatusChange}
              // onAvatarStream={handleAvatarStream} // REMOVED
              // onAvatarVideo={setAvatarVideoUrl} // REMOVED
              onSpeaking={setIsSpeaking}
              enableAvatar={false} // Force Voice Only
            />
          )}
        </div>
      </section>
    </div>
  );
}
