
export const normalizeApiBase = (rawUrl: string | undefined, fallback: string): string => {
  const isBrowser = typeof window !== 'undefined';
  let url = (rawUrl || fallback).trim();

  // Strip leading/trailing quotes (fixes env var injection issues)
  url = url.replace(/^['"]|['"]$/g, '');

  // Convert HTTP to HTTPS when the page is loaded over HTTPS (case-insensitive)
  if (isBrowser && window.location.protocol === 'https:' && /^http:\/\//i.test(url)) {
    url = url.replace(/^http:\/\//i, 'https://');
  }

  // FORCE HTTPS for production API domain (bypasses any other logic)
  if (url.includes('api.ctxeco.com')) {
    url = url.replace(/^http:\/\//i, 'https://');
  }

  url = url.replace(/\/$/, '');
  url = url.replace(/\/api\/v1\/?$/i, '');

  return url;
};
