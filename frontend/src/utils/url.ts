export const normalizeApiBase = (rawUrl: string | undefined, fallback: string): string => {
  const isBrowser = typeof window !== 'undefined';
  let url = (rawUrl || fallback).trim();

  if (isBrowser && window.location.protocol === 'https:' && url.startsWith('http://')) {
    url = url.replace(/^http:\/\//, 'https://');
  }

  url = url.replace(/\/$/, '');
  url = url.replace(/\/api\/v1\/?$/i, '');

  return url;
};
