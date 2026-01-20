/**
 * RTClientAvatar.ts
 * 
 * Avatar client using Microsoft's rt-client package for VoiceLive Avatar.
 * This replaces the broken AvatarSynthesizer approach.
 */

import { RTClient } from 'rt-client';
import type { Voice, Modality } from 'rt-client';
import { normalizeApiBase } from '../../utils/url';
import { getAccessToken } from '../../auth/authConfig';

export interface RTClientAvatarConfig {
    endpoint: string;
    apiKey?: string;
    model?: string;
    voice?: string | Voice;
    instructions?: string;
    avatarCharacter?: string;
    avatarStyle?: string;
}

export class RTClientAvatar {
    private client: RTClient | null = null;
    private peerConnection: RTCPeerConnection | null = null;
    private _isConnected = false;
    private onStream: ((stream: MediaStream) => void) | null = null;
    private videoElement: HTMLVideoElement | null = null;
    private audioElement: HTMLAudioElement | null = null;

    constructor(onStream?: (stream: MediaStream) => void) {
        this.onStream = onStream || null;
    }

    public get isConnected(): boolean {
        return this._isConnected;
    }

    /**
     * Connect to VoiceLive Avatar service
     */
    public async connect(config: RTClientAvatarConfig): Promise<void> {
        if (this._isConnected) return;

        try {
            console.log('RTClientAvatar: Connecting...');

            // Get auth token if needed
            const authToken = await getAccessToken().catch(() => null);
            const clientAuth = config.apiKey
                ? { key: config.apiKey }
                : authToken
                    ? { getToken: async () => ({ token: authToken!, expiresOnTimestamp: Date.now() + 3600000 }) }
                    : { key: '' };

            // Create RTClient
            this.client = new RTClient(
                new URL(config.endpoint),
                clientAuth,
                {
                    modelOrAgent: config.model || 'gpt-realtime',
                    apiVersion: '2026-01-01-preview'
                }
            );

            console.log('RTClientAvatar: Client created, configuring session...');

            // Configure session with avatar
            const voice: Voice = typeof config.voice === 'string'
                ? { name: config.voice, type: 'azure-standard' }
                : config.voice || { name: 'en-US-AvaMultilingualNeural', type: 'azure-standard' };

            const modalities: Modality[] = ['text', 'audio'];

            const session = await this.client.configure({
                instructions: config.instructions || 'You are a helpful AI assistant.',
                input_audio_transcription: {
                    model: 'azure-speech',
                },
                voice,
                avatar: {
                    character: config.avatarCharacter || 'lisa',
                    style: config.avatarStyle || 'casual-sitting',
                    video: {
                        codec: 'h264',
                        crop: {
                            top_left: [560, 0],
                            bottom_right: [1360, 1080],
                        },
                    },
                },
                modalities,
                turn_detection: {
                    type: 'server_vad',
                },
            });

            console.log('RTClientAvatar: Session configured, session id:', session.id);

            // Setup WebRTC connection if avatar ICE servers provided
            if (session?.avatar?.ice_servers) {
                await this.setupWebRTC(session.avatar.ice_servers);
            }

            // Start event listener
            this.startEventListener();

            this._isConnected = true;
            console.log('RTClientAvatar: Connected successfully');

        } catch (e) {
            console.error('RTClientAvatar: Connection failed', e);
            throw e;
        }
    }

    /**
     * Setup WebRTC peer connection for avatar video
     */
    private async setupWebRTC(iceServers: RTCIceServer[]): Promise<void> {
        console.log('RTClientAvatar: Setting up WebRTC with ICE servers:', JSON.stringify(iceServers));

        // Create peer connection
        this.peerConnection = new RTCPeerConnection({ iceServers });

        // Setup track handler
        this.peerConnection.ontrack = (event) => {
            console.log('RTClientAvatar: ontrack fired!', event.track.kind, event.streams?.length);
            const stream = event.streams?.[0];
            if (!stream) return;

            if (event.track.kind === 'video') {
                console.log('RTClientAvatar: Received video track');
                this.onStream?.(stream);

                if (!this.videoElement) {
                    this.videoElement = document.createElement('video');
                    this.videoElement.id = 'rtclient-avatar-video';
                    this.videoElement.autoplay = true;
                    this.videoElement.playsInline = true;
                    this.videoElement.muted = true; // Mute video element, audio comes from audio track
                    this.videoElement.style.display = 'none';
                    document.body.appendChild(this.videoElement);
                }
                this.videoElement.srcObject = stream;
                this.videoElement.play().catch(() => { });
            } else if (event.track.kind === 'audio') {
                console.log('RTClientAvatar: Received audio track');
                if (!this.audioElement) {
                    this.audioElement = document.createElement('audio');
                    this.audioElement.id = 'rtclient-avatar-audio';
                    this.audioElement.autoplay = true;
                    document.body.appendChild(this.audioElement);
                }
                this.audioElement.srcObject = stream;
                this.audioElement.play().catch(() => { });
            }
        };

        // Add transceivers
        this.peerConnection.addTransceiver('video', { direction: 'sendrecv' });
        this.peerConnection.addTransceiver('audio', { direction: 'sendrecv' });

        // Create data channel for events
        this.peerConnection.createDataChannel('eventChannel');

        // Log ICE state changes
        this.peerConnection.oniceconnectionstatechange = () => {
            console.log('RTClientAvatar: ICE connection state:', this.peerConnection?.iceConnectionState);
        };
        this.peerConnection.onsignalingstatechange = () => {
            console.log('RTClientAvatar: Signaling state:', this.peerConnection?.signalingState);
        };

        // Create offer
        const sdp = await this.peerConnection.createOffer();
        await this.peerConnection.setLocalDescription(sdp);
        console.log('RTClientAvatar: Local description set, waiting for ICE gathering...');

        // Wait for ICE candidates to be gathered
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Get remote description from server via connectAvatar
        console.log('RTClientAvatar: Calling connectAvatar...');
        const remoteDescription = await this.client?.connectAvatar(
            this.peerConnection.localDescription as RTCSessionDescription
        );

        if (remoteDescription) {
            console.log('RTClientAvatar: Received remote description, setting...');
            await this.peerConnection.setRemoteDescription(remoteDescription as RTCSessionDescriptionInit);
            console.log('RTClientAvatar: WebRTC connected!');
        } else {
            console.error('RTClientAvatar: No remote description received');
        }
    }

    /**
     * Start listening for events from the server
     */
    private async startEventListener(): Promise<void> {
        if (!this.client) return;

        try {
            for await (const event of this.client.events()) {
                if (event.type === 'response') {
                    console.log('RTClientAvatar: Response received');
                } else if (event.type === 'input_audio') {
                    console.log('RTClientAvatar: Input audio received');
                }
            }
        } catch (error) {
            if (this.client) {
                console.error('RTClientAvatar: Event listener error:', error);
            }
        }
    }

    /**
     * Send a text message and trigger response
     */
    public async sendMessage(text: string): Promise<void> {
        if (!this.client) return;

        try {
            await this.client.sendItem({
                type: 'message',
                role: 'user',
                content: [{ type: 'input_text', text }],
            });
            await this.client.generateResponse();
        } catch (e) {
            console.error('RTClientAvatar: Failed to send message:', e);
        }
    }

    /**
     * Alias for sendMessage - triggers avatar to speak the given text
     */
    public async speak(text: string): Promise<void> {
        return this.sendMessage(text);
    }

    /**
     * Disconnect from the service
     */
    public async disconnect(): Promise<void> {
        if (this.client) {
            try {
                await this.client.close();
            } catch {
                // ignore
            }
            this.client = null;
        }

        if (this.peerConnection) {
            try {
                this.peerConnection.close();
            } catch {
                // ignore
            }
            this.peerConnection = null;
        }

        if (this.videoElement) {
            this.videoElement.srcObject = null;
            this.videoElement.remove();
            this.videoElement = null;
        }

        if (this.audioElement) {
            this.audioElement.srcObject = null;
            this.audioElement.remove();
            this.audioElement = null;
        }

        this._isConnected = false;
        console.log('RTClientAvatar: Disconnected');
    }
}
