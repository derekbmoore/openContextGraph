import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { VoiceInteractionPage } from './VoiceInteractionPage';

// Mock the VoiceChat component
vi.mock('../../components/VoiceChat/VoiceChat', () => ({
  default: ({ agentId }: { agentId: string }) => (
    <div data-testid="voice-chat-mock">VoiceChat Component for {agentId}</div>
  ),
}));

describe('VoiceInteractionPage', () => {
  it('should render agent info for Elena', () => {
    render(<VoiceInteractionPage activeAgent="elena" sessionId="test-session" />);
    expect(screen.getByRole('heading', { name: /dr\. elena vasquez/i })).toBeInTheDocument();
    expect(screen.getByText(/business analyst/i)).toBeInTheDocument();
  });

  it('should render agent info for Marcus', () => {
    render(<VoiceInteractionPage activeAgent="marcus" sessionId="test-session" />);
    expect(screen.getByRole('heading', { name: /marcus chen/i })).toBeInTheDocument();
    expect(screen.getByText(/project manager/i)).toBeInTheDocument();
  });

  it('should require activation before rendering VoiceChat', () => {
    render(<VoiceInteractionPage activeAgent="elena" sessionId="test-session" />);
    expect(screen.queryByTestId('voice-chat-mock')).not.toBeInTheDocument();
    const activateButton = screen.getByRole('button', { name: /activate voice/i });
    fireEvent.click(activateButton);
    expect(screen.getByTestId('voice-chat-mock')).toBeInTheDocument();
  });

  it('should pass correct agent ID to VoiceChat after activation', () => {
    render(<VoiceInteractionPage activeAgent="marcus" sessionId="test-session" />);
    fireEvent.click(screen.getByRole('button', { name: /activate voice/i }));
    expect(screen.getByText(/voicechat component for marcus/i)).toBeInTheDocument();
  });
});
