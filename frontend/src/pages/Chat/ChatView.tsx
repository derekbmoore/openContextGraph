import { useState } from 'react';
import { ChatPanel } from '../../components/ChatPanel/ChatPanel';
import { AvatarCenterPanel } from '../../components/AvatarCenterPanel/AvatarCenterPanel';
import { useOutletContext } from 'react-router-dom';
import type { Agent } from '../../types';

interface ChatViewContext {
    agent: Agent;
    selectedModel: string;
    onModelChange: (model: string) => void;
    sessionId: string;
}

export function ChatView() {
    const { agent, selectedModel, onModelChange, sessionId } = useOutletContext<ChatViewContext>();

    // Metrics state (kept for ChatPanel compatibility, even if VisualPanel is removed)
    const [sessionMetrics, setSessionMetrics] = useState({
        tokensUsed: 0,
        latency: 0,
        memoryNodes: 0,
        duration: 0,
        turns: 0,
        cost: 0
    });

    return (
        <>
            {/* Middle Column - Chat Interface -> Now Avatar Center */}
            <section className="column column-center">
                <AvatarCenterPanel
                    agent={agent}
                    sessionId={sessionId}
                />
            </section>

            {/* Right Column - Visual Panel -> Now Chat Panel */}
            <aside className="column column-right">
                <ChatPanel
                    key={agent.id}
                    agent={agent}
                    sessionId={sessionId}
                    onMetricsUpdate={setSessionMetrics}
                />
            </aside>
        </>
    );
}
