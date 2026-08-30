import React from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

/**
 * ErrorBoundary catches render-time errors in its child tree and shows a
 * friendly fallback UI instead of a blank white screen. It does NOT catch
 * errors in async callbacks or event handlers (those must be handled with
 * try/catch), so pair this with the api client's ApiError handling.
 */
export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // In production you'd ship this to a monitoring service (Sentry, etc.).
    console.error('[ErrorBoundary] Render error:', error, errorInfo);
  }

  handleReload = () => {
    this.setState({ hasError: false, error: null });
    // Force a clean remount of the child route by reloading the page.
    if (typeof window !== 'undefined') window.location.reload();
  };

  handleHome = () => {
    this.setState({ hasError: false, error: null });
    if (typeof window !== 'undefined') window.location.href = '/';
  };

  render() {
    if (!this.state.hasError) return this.props.children;

    const message =
      this.state.error && this.state.error.message
        ? String(this.state.error.message)
        : 'An unexpected error occurred while rendering this page.';

    return (
      <div className="min-h-[60vh] flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-card border border-border rounded-2xl shadow-sm p-8 text-center">
          <div className="mx-auto w-14 h-14 rounded-full bg-red-100 flex items-center justify-center mb-4">
            <AlertTriangle className="w-7 h-7 text-red-600" />
          </div>
          <h2 className="text-xl font-semibold text-primary mb-2">Something went wrong</h2>
          <p className="text-sm text-muted-foreground mb-6">{message}</p>
          <div className="flex gap-3 justify-center">
            <button
              onClick={this.handleReload}
              className="inline-flex items-center gap-2 bg-primary hover:bg-primary/90 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              Reload page
            </button>
            <button
              onClick={this.handleHome}
              className="inline-flex items-center gap-2 bg-muted hover:bg-muted/70 text-foreground px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              <Home className="w-4 h-4" />
              Go home
            </button>
          </div>
        </div>
      </div>
    );
  }
}
