export const normalizeApiBase = (rawUrl: string | undefined, fallback: string): string => {
  const isBrowser = typeof window !== 'undefined';
  let url = (rawUrl || fallback).trim();

  // Convert HTTP to HTTPS when the page is loaded over HTTPS (case-insensitive)
  if (isBrowser && window.location.protocol === 'https:' && /^http:\/\//i.test(url)) {
    url = url.replace(/^http:\/\//i, 'https://');
  }

  url = url.replace(/\/$/, '');
  url = url.replace(/\/api\/v1\/?$/i, '');

  return url;
};
