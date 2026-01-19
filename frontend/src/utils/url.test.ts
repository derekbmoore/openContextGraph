import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { normalizeApiBase } from './url';

describe('normalizeApiBase', () => {
  let originalWindow: typeof window;
  let originalLocation: Location;

  beforeEach(() => {
    // Store original window and location
    originalWindow = global.window as typeof window;
    originalLocation = global.window?.location;
  });

  afterEach(() => {
    // Restore original window and location
    if (originalWindow) {
      global.window = originalWindow;
    }
  });

  it('should convert http:// to https:// when page is loaded over HTTPS', () => {
    // Mock browser environment with HTTPS
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('http://api.ctxeco.com', 'https://fallback.com');
    expect(result).toBe('https://api.ctxeco.com');
  });

  it('should convert HTTP:// (uppercase) to https:// when page is loaded over HTTPS', () => {
    // Mock browser environment with HTTPS
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('HTTP://api.ctxeco.com', 'https://fallback.com');
    expect(result).toBe('https://api.ctxeco.com');
  });

  it('should convert Http:// (mixed case) to https:// when page is loaded over HTTPS', () => {
    // Mock browser environment with HTTPS
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('Http://api.ctxeco.com', 'https://fallback.com');
    expect(result).toBe('https://api.ctxeco.com');
  });

  it('should not convert http:// to https:// when page is loaded over HTTP', () => {
    // Mock browser environment with HTTP
    global.window = {
      location: {
        protocol: 'http:',
        origin: 'http://localhost:3000',
      },
    } as any;

    const result = normalizeApiBase('http://api.ctxeco.com', 'http://fallback.com');
    expect(result).toBe('http://api.ctxeco.com');
  });

  it('should keep https:// URLs unchanged', () => {
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('https://api.ctxeco.com', 'https://fallback.com');
    expect(result).toBe('https://api.ctxeco.com');
  });

  it('should use fallback when rawUrl is undefined', () => {
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase(undefined, 'https://fallback.com');
    expect(result).toBe('https://fallback.com');
  });

  it('should use fallback when rawUrl is empty string', () => {
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('', 'https://fallback.com');
    expect(result).toBe('https://fallback.com');
  });

  it('should remove trailing slash', () => {
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('https://api.ctxeco.com/', 'https://fallback.com');
    expect(result).toBe('https://api.ctxeco.com');
  });

  it('should remove /api/v1 suffix', () => {
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('https://api.ctxeco.com/api/v1', 'https://fallback.com');
    expect(result).toBe('https://api.ctxeco.com');
  });

  it('should remove /api/v1/ suffix with trailing slash', () => {
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('https://api.ctxeco.com/api/v1/', 'https://fallback.com');
    expect(result).toBe('https://api.ctxeco.com');
  });

  it('should handle mixed case /API/V1 suffix', () => {
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('https://api.ctxeco.com/API/V1', 'https://fallback.com');
    expect(result).toBe('https://api.ctxeco.com');
  });

  it('should trim whitespace from URL', () => {
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('  https://api.ctxeco.com  ', 'https://fallback.com');
    expect(result).toBe('https://api.ctxeco.com');
  });

  it('should handle http:// with uppercase on HTTPS page and convert correctly', () => {
    global.window = {
      location: {
        protocol: 'https:',
        origin: 'https://ctxeco.com',
      },
    } as any;

    const result = normalizeApiBase('HTTP://API.CTXECO.COM/api/v1/', 'https://fallback.com');
    expect(result).toBe('https://API.CTXECO.COM');
  });

  it('should work in non-browser environment', () => {
    // Remove window to simulate non-browser environment
    delete (global as any).window;

    const result = normalizeApiBase('http://api.ctxeco.com', 'http://fallback.com');
    // In non-browser environment, HTTP shouldn't be converted to HTTPS
    expect(result).toBe('http://api.ctxeco.com');
  });
});
