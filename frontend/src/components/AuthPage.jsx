import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Mail, Lock, User, Loader2, LogIn, UserPlus } from 'lucide-react';
import { useAuth } from '../lib/auth';

/**
 * Combined login/register page. Toggles between modes. On success the user is
 * redirected to the home route.
 */
export default function AuthPage() {
  const [mode, setMode] = useState('login'); // 'login' | 'register'
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, register, loading } = useAuth();
  const navigate = useNavigate();

  const switchMode = (next) => {
    setMode(next);
    setUsername('');
    setPassword('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result =
      mode === 'login'
        ? await login({ email, password })
        : await register({ email, username, password });
    if (result.ok) navigate('/home');
  };

  return (
    <div className="max-w-md mx-auto mt-8">
      <div className="bg-card border border-border rounded-2xl shadow-sm p-8">
        <div className="flex items-center justify-center mb-6">
          <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
            {mode === 'login' ? (
              <LogIn className="w-6 h-6 text-primary" />
            ) : (
              <UserPlus className="w-6 h-6 text-primary" />
            )}
          </div>
        </div>
        <h2 className="text-2xl font-bold text-center text-primary mb-1">
          {mode === 'login' ? 'Welcome back' : 'Create your account'}
        </h2>
        <p className="text-center text-sm text-muted-foreground mb-6">
          {mode === 'login'
            ? 'Log in to sync your learning paths across devices.'
            : 'Sign up to save your progress and personalize recommendations.'}
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Email</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-border focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent bg-white"
              />
            </div>
          </div>

          {mode === 'register' && (
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Username</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  type="text"
                  required
                  minLength={3}
                  maxLength={32}
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="yourname"
                  className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-border focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent bg-white"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                type="password"
                required
                minLength={mode === 'register' ? 8 : 1}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={mode === 'register' ? 'At least 8 characters' : '••••••••'}
                className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-border focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent bg-white"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-primary text-white rounded-lg font-medium hover:bg-primary/90 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loading ? (
              <><Loader2 className="w-4 h-4 animate-spin" /> Please wait...</>
            ) : mode === 'login' ? (
              <><LogIn className="w-4 h-4" /> Log in</>
            ) : (
              <><UserPlus className="w-4 h-4" /> Create account</>
            )}
          </button>
        </form>

        <p className="text-center text-sm text-muted-foreground mt-6">
          {mode === 'login' ? "Don't have an account? " : 'Already have an account? '}
          <button
            onClick={() => switchMode(mode === 'login' ? 'register' : 'login')}
            className="text-primary hover:underline font-medium"
          >
            {mode === 'login' ? 'Sign up' : 'Log in'}
          </button>
        </p>

        <p className="text-center text-xs text-muted-foreground mt-4">
          <Link to="/home" className="hover:underline">Continue without an account</Link>
        </p>
      </div>
    </div>
  );
}
