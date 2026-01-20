/**
 * AvatarClient.ts
 * 
 * Wrapper around Azure Speech SDK to handle Text-to-Speech Avatar.
 * Manages authentication (via backend STS) and video rendering.
 */

import * as SpeechSDK from 'microsoft-cognitiveservices-speech-sdk';
import { normalizeApiBase } from '../../utils/url';
import { getAccessToken } from '../../auth/authConfig';

export class AvatarClient {
    private connector: any | null = null; // SpeechSDK.AvatarSynthesizer (SDK typing may lag)
    private element: HTMLDivElement | null = null;
    private _isConnected = false;
    private pc: RTCPeerConnection | null = null;
    private onStream: ((stream: MediaStream) => void) | null = null;
    private audioElement: HTMLAudioElement | null = null;

    constructor(targetElement: HTMLDivElement | null, onStream?: (stream: MediaStream) => void) {
        this.element = targetElement;
        this.onStream = onStream || null;
    }

    public get isConnected(): boolean {
        return this._isConnected;
    }

    public async fetchToken(): Promise<{ token: string; region: string }> {
        const baseUrl = normalizeApiBase(import.meta.env.VITE_API_URL as string | undefined, window.location.origin);
        const authToken = await getAccessToken();

        const response = await fetch(`${baseUrl}/api/v1/voice/avatar/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch avatar token: ${response.status}`);
        }

        return response.json();
    }

    public async connect(
        authData: { token: string; region: string }
    ): Promise<void> {
        if (this._isConnected) return;

        try {
            console.log('AvatarClient: Connecting...');

            const { token, region } = authData;

            // 1. Configure Speech SDK
            const speechConfig = SpeechSDK.SpeechConfig.fromAuthorizationToken(token, region);
            // Note: voice name here is Speech TTS voice name (not VoiceLive DragonHD name).
            speechConfig.speechSynthesisVoiceName = 'en-US-AvaMultilingualNeural';

            // 2. Configure Avatar (feature-gated because SDK typing/features can vary by version)
            // Using 'any' cast because TS definitions might be out of sync with experimental Avatar SDK features
            // Robust check: ensure constructors exist
            let avatarConfig: any;
            try {
                const sdkAny = SpeechSDK as any;
                if (sdkAny.AvatarVideoFormat && sdkAny.AvatarConfig) {
                    const videoFormat = new sdkAny.AvatarVideoFormat(1920, 1080);
                    avatarConfig = new sdkAny.AvatarConfig('lisa', 'graceful', videoFormat);
                } else if (sdkAny.AvatarConfig) {
                    console.warn("AvatarClient: AvatarVideoFormat not found, trying 2-arg AvatarConfig");
                    avatarConfig = new sdkAny.AvatarConfig('lisa', 'graceful');
                } else {
                    throw new Error("AvatarConfig not found in SpeechSDK");
                }
            } catch (configError) {
                console.error("AvatarClient: Failed to create AvatarConfig", configError);
                throw configError;
            }

            // 3. Create Avatar Synthesizer
            const sdkAny = SpeechSDK as any;
            if (!sdkAny.AvatarSynthesizer) {
                throw new Error("AvatarSynthesizer not found in SpeechSDK (SDK version may not support avatar).");
            }
            this.connector = new sdkAny.AvatarSynthesizer(speechConfig, avatarConfig);

            // 4. Setup WebRTC Peer Connection (browser-side)
            // Provide TURN config via backend ICE endpoint (most reliable behind NAT/corp firewalls).
            const iceConfig = await this.fetchIceCredentials();

            const pc = new RTCPeerConnection({
                iceServers: (iceConfig?.ice_servers?.length ? iceConfig.ice_servers : undefined) || [
                    { urls: "stun:stun.l.google.com:19302" } // Fallback (dev only)
                ],
                // NOTE: relay-only is safer in corporate networks but can reduce success in permissive NATs.
                // iceTransportPolicy: 'relay',
            });
            this.pc = pc;

            // Debug: Log ICE/Signaling state changes
            pc.oniceconnectionstatechange = () => {
                console.log('AvatarClient: ICE connection state:', pc.iceConnectionState);
            };
            pc.onsignalingstatechange = () => {
                console.log('AvatarClient: Signaling state:', pc.signalingState);
            };
            pc.onconnectionstatechange = () => {
                console.log('AvatarClient: Connection state:', pc.connectionState);
            };
            pc.onicecandidate = (event) => {
                if (event.candidate) {
                    console.log('AvatarClient: ICE candidate:', event.candidate.type, event.candidate.address);
                } else {
                    console.log('AvatarClient: ICE gathering complete');
                }
            };
            pc.onicegatheringstatechange = () => {
                console.log('AvatarClient: ICE gathering state:', pc.iceGatheringState);
            };

            // Receive tracks (video + audio) from Avatar Relay
            pc.ontrack = (event) => {
                console.log('AvatarClient: ontrack fired!', event.track.kind, event.streams?.length);
                const stream = event.streams?.[0];
                if (!stream) {
                    console.warn('AvatarClient: ontrack but no stream!');
                    return;
                }

                if (event.track.kind === 'video') {
                    console.log('AvatarClient: Received video track');
                    this.onStream?.(stream);

                    if (this.element) {
                        let video = this.element.querySelector('video');
                        if (!video) {
                            video = document.createElement('video');
                            video.autoplay = true;
                            video.playsInline = true;
                            video.muted = true; // avoid feedback if audio track is also present
                            video.style.width = '100%';
                            video.style.height = '100%';
                            video.style.objectFit = 'cover';
                            this.element.appendChild(video);
                        }
                        video.srcObject = stream;
                        video.play().catch(() => { });
                    }
                } else if (event.track.kind === 'audio') {
                    // Play avatar audio (primary POC path). If you want VoiceLive audio instead,
                    // set audioElement.muted=true here and do NOT suppress backend audio.
                    if (!this.audioElement) {
                        this.audioElement = document.createElement('audio');
                        this.audioElement.autoplay = true;
                        this.audioElement.id = 'avatar-audio-player-sdk';
                        // Not muted by default — POC expects avatar audio.
                        document.body.appendChild(this.audioElement);
                    }
                    this.audioElement.srcObject = stream;
                    this.audioElement.play().catch(() => { });
                }
            };

            // Offer to receive one video track, and one audio track (per MS docs)
            pc.addTransceiver('video', { direction: 'sendrecv' });
            pc.addTransceiver('audio', { direction: 'sendrecv' });

            // 5. Start avatar session (SDK performs signaling against Azure Speech Avatar Relay)
            const startFn = this.connector?.startAvatarAsync || this.connector?.startAvatar;
            if (typeof startFn !== 'function') {
                throw new Error("AvatarSynthesizer.startAvatarAsync not available in this Speech SDK version.");
            }

            await new Promise<void>((resolve, reject) => {
                // SDKs differ: some use callbacks, some return Promises. Handle both.
                try {
                    const ret = startFn.call(this.connector, pc, (result: any) => {
                        // Callback-style
                        if (result?.reason === SpeechSDK.ResultReason?.SynthesizingAudioCompleted || result?.reason) {
                            // Not all SDKs return a meaningful ResultReason here; treat callback as success.
                        }
                        this._isConnected = true;
                        resolve();
                    }, (err: any) => {
                        reject(err);
                    });

                    // Promise-style
                    if (ret && typeof ret.then === 'function') {
                        ret.then(() => {
                            this._isConnected = true;
                            resolve();
                        }).catch(reject);
                    }
                } catch (e) {
                    reject(e);
                }
            });

            console.log('AvatarClient: Connected (Avatar session started)');
            console.log('AvatarClient: Post-connect PC state:', {
                signalingState: pc.signalingState,
                iceConnectionState: pc.iceConnectionState,
                iceGatheringState: pc.iceGatheringState,
                connectionState: pc.connectionState,
                localDescription: pc.localDescription?.type,
                remoteDescription: pc.remoteDescription?.type,
            });

        } catch (e) {
            console.error('AvatarClient: Connection failed', e);
            throw e;
        }
    }

    private async fetchIceCredentials(): Promise<any> {
        const baseUrl = normalizeApiBase(import.meta.env.VITE_API_URL as string | undefined, window.location.origin);
        const authToken = await getAccessToken();
        const response = await fetch(`${baseUrl}/api/v1/voice/avatar/ice-credentials`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
            },
            body: JSON.stringify({ agent_id: 'elena' })
        });
        if (response.ok) {
            const data = await response.json();
            return {
                ice_servers: [{
                    urls: data.urls,
                    username: data.username,
                    credential: data.credential,
                }]
            };
        }
        return { ice_servers: [] };
    }


    public async speak(text: string): Promise<void> {
        if (!this.connector) return;
        if (!text?.trim()) return;

        console.log('AvatarClient: Speaking...', text.substring(0, 30));

        return new Promise((resolve, reject) => {
            // Cast to any to allow 3-argument signature (text, successCb, errorCb)
            (this.connector as any).speakTextAsync(
                text,
                (result: any) => {
                    if (result.reason === SpeechSDK.ResultReason.SynthesizingAudioCompleted) {
                        console.log("AvatarClient: Speech complete.");
                        resolve();
                    } else {
                        console.error("AvatarClient: Speech failed or canceled", result.errorDetails);
                        reject(result.errorDetails);
                    }
                },
                (error: any) => {
                    console.error("AvatarClient: Speak error", error);
                    reject(error);
                }
            );
        });
    }

    public disconnect() {
        if (this.connector) {
            this.connector.close();
            this.connector = null;
        }
        if (this.pc) {
            try {
                this.pc.close();
            } catch {
                // ignore
            }
            this.pc = null;
        }
        if (this.audioElement) {
            try {
                this.audioElement.pause();
                this.audioElement.srcObject = null;
                this.audioElement.remove();
            } catch {
                // ignore
            }
            this.audioElement = null;
        }
        this._isConnected = false;
    }
}
