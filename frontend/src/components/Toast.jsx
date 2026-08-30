import React, { createContext, useCallback, useContext, useState, useRef } from 'react';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

// Lightweight toast notification system. Components call `toast.success(msg)`
// or `toast.error(msg)` and the provider renders stacked notifications.

const ToastContext = createContext(null);

let idCounter = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const timers = useRef({});

  const dismiss = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
    if (timers.current[id]) {
      clearTimeout(timers.current[id]);
      delete timers.current[id];
    }
  }, []);

  const push = useCallback((type, message, { duration = 5000 } = {}) => {
    const id = ++idCounter;
    setToasts((prev) => [...prev, { id, type, message }]);
    if (duration > 0) {
      timers.current[id] = setTimeout(() => dismiss(id), duration);
    }
    return id;
  }, [dismiss]);

  const toast = {
    success: (msg, opts) => push('success', msg, opts),
    error: (msg, opts) => push('error', msg, opts),
    info: (msg, opts) => push('info', msg, opts),
    dismiss,
  };

  return (
    <ToastContext.Provider value={toast}>
      {children}
      <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none">
        {toasts.map((t) => (
          <ToastItem key={t.id} toast={t} onClose={() => dismiss(t.id)} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

const ICONS = {
  success: CheckCircle2,
  error: AlertCircle,
  info: Info,
};

const STYLES = {
  success: 'bg-green-50 border-green-200 text-green-800',
  error: 'bg-red-50 border-red-200 text-red-800',
  info: 'bg-blue-50 border-blue-200 text-blue-800',
};

function ToastItem({ toast, onClose }) {
  const Icon = ICONS[toast.type] || Info;
  return (
    <div
      className={`pointer-events-auto flex items-start gap-3 border rounded-xl shadow-sm p-4 animate-in fade-in slide-in-from-top-2 ${STYLES[toast.type]}`}
      role="alert"
    >
      <Icon className="w-5 h-5 mt-0.5 flex-shrink-0" />
      <p className="text-sm flex-1">{toast.message}</p>
      <button onClick={onClose} className="flex-shrink-0 opacity-60 hover:opacity-100 transition-opacity">
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) {
    // Graceful no-op if used outside a provider (e.g. in isolated tests).
    return {
      success: (m) => console.info('[toast.success]', m),
      error: (m) => console.error('[toast.error]', m),
      info: (m) => console.info('[toast.info]', m),
      dismiss: () => {},
    };
  }
  return ctx;
}
