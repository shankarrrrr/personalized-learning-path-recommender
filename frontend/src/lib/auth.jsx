import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { api, ApiError, describeError } from '../lib/api';
import { useToast } from '../components/Toast';

// Auth context: stores the current user + token, and exposes login/register/logout.
// The token is persisted in localStorage so a page refresh keeps you logged in.

const AuthContext = createContext(null);

const TOKEN_KEY = 'auth_token';
const USER_KEY = 'auth_user';

function readStoredUser() {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => {
    try { return localStorage.getItem(TOKEN_KEY) || null; } catch { return null; }
  });
  const [user, setUser] = useState(readStoredUser);
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  // Attach the bearer token to every future API request when present.
  useEffect(() => {
    if (token) {
      api.defaults = api.defaults || {};
    }
  }, [token]);

  const persist = (tok, u) => {
    setToken(tok);
    setUser(u);
    try {
      if (tok) localStorage.setItem(TOKEN_KEY, tok); else localStorage.removeItem(TOKEN_KEY);
      if (u) localStorage.setItem(USER_KEY, JSON.stringify(u)); else localStorage.removeItem(USER_KEY);
    } catch {
      /* ignore storage errors */
    }
  };

  const register = useCallback(async ({ email, username, password }) => {
    setLoading(true);
    try {
      const data = await api.post('/auth/register', { email, username, password });
      persist(data.access_token, data.user);
      toast.success(`Welcome, ${data.user.username}! Your account is ready.`);
      return { ok: true };
    } catch (err) {
      const msg = describeError(err);
      toast.error(msg);
      return { ok: false, error: msg };
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const login = useCallback(async ({ email, password }) => {
    setLoading(true);
    try {
      const data = await api.post('/auth/login', { email, password });
      persist(data.access_token, data.user);
      toast.success(`Welcome back, ${data.user.username}!`);
      return { ok: true };
    } catch (err) {
      const msg = describeError(err);
      toast.error(msg);
      return { ok: false, error: msg };
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const logout = useCallback(() => {
    persist(null, null);
    toast.info('You have been logged out.');
  }, [toast]);

  return (
    <AuthContext.Provider value={{ token, user, loading, register, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    return {
      token: null, user: null, loading: false,
      register: async () => ({ ok: false, error: 'auth unavailable' }),
      login: async () => ({ ok: false, error: 'auth unavailable' }),
      logout: () => {}, isAuthenticated: false,
    };
  }
  return ctx;
}
