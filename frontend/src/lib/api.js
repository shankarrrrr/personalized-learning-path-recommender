// Centralized API client for the Personalized Learning Path Recommender.
// All frontend network calls should go through this module so error handling,
// base URL configuration and timeout behaviour stay consistent.
//
// The backend returns errors in a normalized shape:
//   { "error": "<code>", "message": "<human readable>", "detail": {...} }
// This client turns non-2xx responses into ApiError instances carrying that
// payload, so components can render actionable messages.

const API_BASE_URL =
  (import.meta && import.meta.env && import.meta.env.VITE_API_BASE_URL) ||
  'http://127.0.0.1:8000';

// Default request timeout (ms). Backend AI calls can be slow, so keep it generous.
const DEFAULT_TIMEOUT = 30000;

export class ApiError extends Error {
  constructor(message, { status = 0, code = 'unknown', detail = null } = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
    this.detail = detail;
  }
}

function isAbortError(err) {
  return err && err.name === 'AbortError';
}

async function parseError(response) {
  // Try to read the structured error body; fall back to status text.
  let body = null;
  try {
    body = await response.json();
  } catch (_) {
    // Non-JSON body (e.g. plain text from a proxy).
  }
  if (body && body.error) {
    return new ApiError(body.message || 'Request failed', {
      status: response.status,
      code: body.error,
      detail: body.detail || null,
    });
  }
  return new ApiError(
    `Request failed with status ${response.status}`,
    { status: response.status, code: 'http_error' }
  );
}

/**
 * Core request function used by all verb helpers.
 * @param {string} path - Path appended to API_BASE_URL (leading slash optional).
 * @param {object} options - fetch options plus { timeoutMs, body, query }.
 * @returns {Promise<any>} Parsed JSON response.
 */
export async function apiRequest(path, options = {}) {
  const {
    method = 'GET',
    body,
    query,
    headers = {},
    timeoutMs = DEFAULT_TIMEOUT,
    signal: externalSignal,
  } = options;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  // If the caller supplied a signal, abort when it fires too.
  if (externalSignal) {
    if (externalSignal.aborted) controller.abort();
    else externalSignal.addEventListener('abort', () => controller.abort());
  }

  let url = path.startsWith('http')
    ? path
    : `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`;

  if (query && Object.keys(query).length > 0) {
    const params = new URLSearchParams();
    for (const [k, v] of Object.entries(query)) {
      if (v === undefined || v === null) continue;
      params.append(k, String(v));
    }
    const qs = params.toString();
    if (qs) url += (url.includes('?') ? '&' : '?') + qs;
  }

  const finalHeaders = { ...headers };
  let payload;
  if (body !== undefined && body !== null) {
    if (body instanceof FormData) {
      payload = body;
    } else {
      finalHeaders['Content-Type'] = finalHeaders['Content-Type'] || 'application/json';
      payload = JSON.stringify(body);
    }
  }

  let response;
  try {
    response = await fetch(url, {
      method,
      headers: finalHeaders,
      body: payload,
      signal: controller.signal,
    });
  } catch (err) {
    clearTimeout(timer);
    if (isAbortError(err)) {
      throw new ApiError('The request took too long and was cancelled. Please try again.', {
        status: 0,
        code: 'timeout',
      });
    }
    // Network error / server unreachable / CORS.
    throw new ApiError('Could not reach the server. Please check your connection and try again.', {
      status: 0,
      code: 'network_error',
    });
  }
  clearTimeout(timer);

  if (!response.ok) {
    throw await parseError(response);
  }

  // 204 No Content
  if (response.status === 204) return null;
  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch (_) {
    return text;
  }
}

export const api = {
  get: (path, options = {}) => apiRequest(path, { ...options, method: 'GET' }),
  post: (path, body, options = {}) => apiRequest(path, { ...options, method: 'POST', body }),
  put: (path, body, options = {}) => apiRequest(path, { ...options, method: 'PUT', body }),
  patch: (path, body, options = {}) => apiRequest(path, { ...options, method: 'PATCH', body }),
  del: (path, options = {}) => apiRequest(path, { ...options, method: 'DELETE' }),
};

/** Human-friendly message for any thrown ApiError (or generic Error). */
export function describeError(err) {
  if (err instanceof ApiError) return err.message;
  if (err && err.message) return err.message;
  return 'Something went wrong. Please try again.';
}
