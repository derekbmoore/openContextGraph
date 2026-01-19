import { normalizeApiBase } from '../utils/url';
import type { AgentId } from '../types';

export interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
}

export interface ChatResponse {
    response: string;
    session_id: string;
    agent: string;
    sources?: string[];
    tool_calls?: Array<Record<string, unknown>>;
}

export class ChatService {
    private static instance: ChatService;
    private apiBase: string;

    private constructor() {
        // Strictly normalize API Base URL
        const envUrl = import.meta.env.VITE_API_URL as string | undefined;
        const isBrowser = typeof window !== 'undefined';
        const fallback = isBrowser ? window.location.origin : 'http://localhost:8082';

        // Use the normalized URL which now includes strict HTTPS for api.ctxeco.com
        this.apiBase = normalizeApiBase(envUrl, fallback);

        // DOUBLE CHECK: Unconditional override if we are in production context
        if (this.apiBase.includes('api.ctxeco.com')) {
            this.apiBase = this.apiBase.replace(/^http:\/\//i, 'https://');
        }
    }

    public static getInstance(): ChatService {
        if (!ChatService.instance) {
            ChatService.instance = new ChatService();
        }
        return ChatService.instance;
    }

    /**
     * Send a message to the chat API
     */
    public async sendMessage(
        message: string,
        agentId: AgentId,
        sessionId?: string
    ): Promise<ChatResponse> {

        const url = `${this.apiBase}/api/v1/chat`;

        console.log(`[ChatService] Sending message to ${url} (Agent: ${agentId})`);

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Add any auth headers here if needed from your auth context
                    // 'Authorization': `Bearer ...`
                },
                body: JSON.stringify({
                    message,
                    agent: agentId,
                    session_id: sessionId
                })
            });

            if (!response.ok) {
                let errorMsg = `API Error: ${response.status}`;
                try {
                    const errorData = await response.json();
                    if (errorData.detail) errorMsg = errorData.detail;
                } catch (e) {
                    // ignore JSON parse error on error response
                }
                throw new Error(errorMsg);
            }

            return await response.json();

        } catch (error) {
            console.error('[ChatService] Request failed:', error);
            throw error;
        }
    }
}

export const chatService = ChatService.getInstance();
