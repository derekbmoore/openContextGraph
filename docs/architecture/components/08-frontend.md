# Frontend — React Application

## Purpose

The Frontend provides the **user interface** for interacting with openContextGraph. Built with React and Vite, it delivers a responsive, accessible experience for chat, memory exploration, and story visualization.

## Why This Exists

### The Problem

AI systems often expose:

- **CLI-only interfaces** that exclude non-technical users
- **Generic chat UIs** that don't leverage the full context system
- **Inaccessible designs** that fail compliance requirements

### The Solution

A purpose-built frontend that:

1. **Surfaces the full context model** (episodic, semantic, operational)
2. **Provides specialized views** for different capabilities
3. **Meets accessibility standards** (WCAG 2.1)
4. **Integrates with identity** for personalized experiences

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Application                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                     Router                              │ │
│  │  /chat  /episodes  /stories  /settings                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐   │
│  │   Chat   │ │ Episodes │ │  Stories │ │   Settings    │   │
│  │  Page    │ │   Page   │ │   Page   │ │     Page      │   │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   Components                            │ │
│  │  ChatInput │ MessageList │ FactCard │ SessionList      │ │
│  │  AgentSelector │ VoiceButton │ Avatar │ Visualizer     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   API Client                            │ │
│  │  /api/v1/chat │ /api/v1/memory │ /api/v1/etl           │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Backend API (FastAPI)
```

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| **React 18** | UI Framework |
| **Vite** | Build tool (fast HMR) |
| **TypeScript** | Type safety |
| **CSS Variables** | Theming |
| **MSAL.js** | Azure AD auth |

---

## Code Samples

### App Entry Point

```typescript
// frontend/src/App.tsx
/**
 * Main Application Component
 * 
 * NIST AI RMF: GOVERN 1.4 (Transparency)
 * - User always knows which agent they're talking to
 * - Context is visible and explorable
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { Layout } from './components/Layout';
import { ChatPage } from './pages/Chat';
import { EpisodesPage } from './pages/Episodes';
import { StoriesPage } from './pages/Stories';

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/episodes" element={<EpisodesPage />} />
            <Route path="/stories" element={<StoriesPage />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  );
}
```

### Chat Component

```typescript
// frontend/src/pages/Chat.tsx
/**
 * Chat Page - Primary interaction interface
 * 
 * NIST AI RMF Controls:
 * - GOVERN 1.4: Agent identity clearly shown
 * - MEASURE 2.5: User feedback collection (thumbs up/down)
 * - MAP 1.1: Context visible in side panel
 */

import { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { ChatInput } from '../components/ChatInput';
import { MessageList } from '../components/MessageList';
import { AgentSelector } from '../components/AgentSelector';
import { ContextPanel } from '../components/ContextPanel';
import { api } from '../api/client';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  agent?: string;
  sources?: string[];
}

export function ChatPage() {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [agent, setAgent] = useState<string>('elena');
  const [sessionId, setSessionId] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  
  async function sendMessage(content: string) {
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content }]);
    setIsLoading(true);
    
    try {
      // Call backend API
      const response = await api.chat({
        message: content,
        session_id: sessionId,
        agent,
      });
      
      // Update session ID
      if (!sessionId) {
        setSessionId(response.session_id);
      }
      
      // Add assistant response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.response,
        agent: response.agent,
        sources: response.sources,
      }]);
      
    } catch (error) {
      console.error('Chat error:', error);
    } finally {
      setIsLoading(false);
    }
  }
  
  return (
    <div className="chat-page">
      <div className="chat-main">
        {/* Agent selector - GOVERN 1.4 transparency */}
        <AgentSelector 
          selected={agent} 
          onChange={setAgent} 
        />
        
        {/* Message list */}
        <MessageList 
          messages={messages} 
          isLoading={isLoading}
        />
        
        {/* Input */}
        <ChatInput 
          onSend={sendMessage}
          disabled={isLoading}
          placeholder={`Ask ${agent}...`}
        />
      </div>
      
      {/* Context panel - MAP 1.1 visibility */}
      <ContextPanel sessionId={sessionId} />
    </div>
  );
}
```

### API Client

```typescript
// frontend/src/api/client.ts
/**
 * API Client for Backend Communication
 * 
 * NIST AI RMF: MANAGE 2.7 (Monitoring)
 * - All requests include timing metrics
 * - Errors are logged for debugging
 */

import { getAccessToken } from '../auth/msal';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8082';

interface ChatRequest {
  message: string;
  session_id?: string;
  agent: string;
}

interface ChatResponse {
  response: string;
  session_id: string;
  agent: string;
  sources: string[];
}

async function request<T>(
  endpoint: string, 
  options: RequestInit = {}
): Promise<T> {
  const token = await getAccessToken();
  
  const start = performance.now();
  
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  });
  
  const duration = performance.now() - start;
  console.debug(`API ${endpoint}: ${duration.toFixed(0)}ms`);
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return response.json();
}

export const api = {
  chat: (data: ChatRequest): Promise<ChatResponse> => 
    request('/api/v1/chat/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  
  searchMemory: (query: string, limit: number = 10) =>
    request(`/api/v1/memory/search`, {
      method: 'POST',
      body: JSON.stringify({ query, limit, search_type: 'hybrid' }),
    }),
  
  listSessions: (userId: string) =>
    request(`/api/v1/memory/sessions/${userId}`),
  
  ingestDocument: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return request('/api/v1/etl/ingest', {
      method: 'POST',
      body: formData,
      headers: {},  // Let browser set Content-Type
    });
  },
};
```

### Context Panel Component

```typescript
// frontend/src/components/ContextPanel.tsx
/**
 * Context Panel - Shows episodic and semantic context
 * 
 * NIST AI RMF: MAP 1.1 (System Context)
 * - Makes AI context visible to users
 * - Shows sources for transparency
 */

import { useState, useEffect } from 'react';
import { api } from '../api/client';

interface Fact {
  content: string;
  source?: string;
  confidence: number;
}

export function ContextPanel({ sessionId }: { sessionId: string }) {
  const [facts, setFacts] = useState<Fact[]>([]);
  const [isOpen, setIsOpen] = useState(true);
  
  useEffect(() => {
    if (sessionId) {
      loadContext();
    }
  }, [sessionId]);
  
  async function loadContext() {
    // Get relevant facts for this session
    const result = await api.searchMemory('session context', 5);
    setFacts(result.results || []);
  }
  
  return (
    <aside className={`context-panel ${isOpen ? 'open' : 'closed'}`}>
      <button onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? '→' : '←'} Context
      </button>
      
      {isOpen && (
        <>
          <h3>Active Context</h3>
          
          <section>
            <h4>Session</h4>
            <code>{sessionId || 'No active session'}</code>
          </section>
          
          <section>
            <h4>Relevant Facts ({facts.length})</h4>
            <ul>
              {facts.map((fact, i) => (
                <li key={i} className="fact-card">
                  <p>{fact.content}</p>
                  {fact.source && (
                    <small>Source: {fact.source}</small>
                  )}
                  <meter value={fact.confidence} min={0} max={1} />
                </li>
              ))}
            </ul>
          </section>
        </>
      )}
    </aside>
  );
}
```

---

## NIST AI RMF Alignment

| Component | Control | Implementation |
|-----------|---------|----------------|
| **AgentSelector** | GOVERN 1.4 | Transparent agent identity |
| **MessageList** | MEASURE 2.5 | Feedback buttons |
| **ContextPanel** | MAP 1.1 | Visible context |
| **API Client** | MANAGE 2.7 | Request timing |

---

## Accessibility (WCAG 2.1)

| Requirement | Implementation |
|-------------|----------------|
| Keyboard navigation | All interactive elements focusable |
| Screen reader | ARIA labels on components |
| Color contrast | 4.5:1 minimum ratio |
| Focus indicators | Visible focus rings |

---

## Summary

The Frontend provides:

- ✅ Purpose-built UI for context-aware AI
- ✅ Multi-agent interface with transparency
- ✅ Context visualization for users
- ✅ Accessibility compliance (WCAG 2.1)
- ✅ NIST AI RMF integration points

*Document Version: 1.0 | Created: 2026-01-11*
