import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { api, ApiError, describeError, apiRequest } from '../lib/api';

// Tests for the centralized API client. fetch is mocked so no network is hit.

describe('api client', () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    global.fetch = vi.fn();
    localStorage.clear();
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  function mockResponse(body, opts = {}) {
    return {
      ok: opts.ok ?? true,
      status: opts.status ?? 200,
      json: async () => body,
      text: async () => (typeof body === 'string' ? body : JSON.stringify(body)),
    };
  }

  describe('api.get', () => {
    it('makes a GET request to the correct URL', async () => {
      global.fetch.mockResolvedValueOnce(mockResponse({ ok: true }));
      await api.get('/health');
      const [url, opts] = global.fetch.mock.calls[0];
      expect(url).toContain('/health');
      expect(opts.method).toBe('GET');
    });

    it('parses JSON response', async () => {
      global.fetch.mockResolvedValueOnce(mockResponse({ foo: 'bar' }));
      const data = await api.get('/anything');
      expect(data).toEqual({ foo: 'bar' });
    });
  });

  describe('api.post', () => {
    it('sends JSON body with Content-Type header', async () => {
      global.fetch.mockResolvedValueOnce(mockResponse({ ok: 1 }));
      await api.post('/onboard', { messages: [] });
      const [, opts] = global.fetch.mock.calls[0];
      expect(opts.method).toBe('POST');
      expect(opts.headers['Content-Type']).toBe('application/json');
      expect(opts.body).toBe(JSON.stringify({ messages: [] }));
    });

    it('attaches bearer token from localStorage when present', async () => {
      localStorage.setItem('auth_token', 'mytoken');
      global.fetch.mockResolvedValueOnce(mockResponse({ ok: 1 }));
      await api.post('/whatever', { x: 1 });
      const [, opts] = global.fetch.mock.calls[0];
      expect(opts.headers['Authorization']).toBe('Bearer mytoken');
    });

    it('does not attach Authorization when no token', async () => {
      global.fetch.mockResolvedValueOnce(mockResponse({ ok: 1 }));
      await api.get('/x');
      const [, opts] = global.fetch.mock.calls[0];
      expect(opts.headers['Authorization']).toBeUndefined();
    });
  });

  describe('query params', () => {
    it('appends query params to the URL', async () => {
      global.fetch.mockResolvedValueOnce(mockResponse({}));
      await api.get('/careers', { query: { domain: 'Data', limit: 5 } });
      const url = global.fetch.mock.calls[0][0];
      expect(url).toContain('domain=Data');
      expect(url).toContain('limit=5');
    });

    it('skips undefined/null query values', async () => {
      global.fetch.mockResolvedValueOnce(mockResponse({}));
      await api.get('/careers', { query: { a: 1, b: undefined, c: null } });
      const url = global.fetch.mock.calls[0][0];
      expect(url).toContain('a=1');
      expect(url).not.toContain('b=');
      expect(url).not.toContain('c=');
    });
  });

  describe('error handling', () => {
    it('throws ApiError on non-2xx with structured payload', async () => {
      global.fetch.mockResolvedValueOnce(
        mockResponse({ error: 'validation_error', message: 'Bad', detail: { x: 1 } }, { ok: false, status: 422 })
      );
      await expect(api.get('/bad')).rejects.toMatchObject({
        name: 'ApiError',
        status: 422,
        code: 'validation_error',
        message: 'Bad',
      });
    });

    it('throws ApiError on network failure', async () => {
      global.fetch.mockRejectedValueOnce(new TypeError('Failed to fetch'));
      await expect(api.get('/x')).rejects.toMatchObject({
        name: 'ApiError',
        code: 'network_error',
      });
    });

    it('throws timeout ApiError when abort fires', async () => {
      global.fetch.mockRejectedValueOnce(new DOMException('Aborted', 'AbortError'));
      await expect(api.get('/x', { timeoutMs: 1 })).rejects.toMatchObject({
        code: 'timeout',
      });
    });
  });

  describe('describeError helper', () => {
    it('returns ApiError message', () => {
      const e = new ApiError('boom', { status: 500, code: 'internal_error' });
      expect(describeError(e)).toBe('boom');
    });

    it('returns generic message for unknown errors', () => {
      expect(describeError(new Error('x'))).toBe('x');
      expect(describeError(null)).toContain('Something went wrong');
    });
  });
});
