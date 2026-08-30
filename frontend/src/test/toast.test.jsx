import React from 'react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { ToastProvider, useToast } from '../components/Toast';

// Helper component that exposes the toast API inside the provider.
function ToastTrigger() {
  const toast = useToast();
  return (
    <div>
      <button onClick={() => toast.success('Success!')}>fire-success</button>
      <button onClick={() => toast.error('Error!')}>fire-error</button>
      <button onClick={() => toast.info('Info!')}>fire-info</button>
    </div>
  );
}

describe('Toast system', () => {
  it('renders nothing initially', () => {
    render(
      <ToastProvider>
        <ToastTrigger />
      </ToastProvider>
    );
    expect(screen.queryByRole('alert')).toBeNull();
  });

  it('shows a success toast when triggered', () => {
    render(
      <ToastProvider>
        <ToastTrigger />
      </ToastProvider>
    );
    act(() => {
      screen.getByText('fire-success').click();
    });
    expect(screen.getByText('Success!')).toBeInTheDocument();
  });

  it('shows an error toast when triggered', () => {
    render(
      <ToastProvider>
        <ToastTrigger />
      </ToastProvider>
    );
    act(() => {
      screen.getByText('fire-error').click();
    });
    expect(screen.getByText('Error!')).toBeInTheDocument();
  });

  it('shows an info toast when triggered', () => {
    render(
      <ToastProvider>
        <ToastTrigger />
      </ToastProvider>
    );
    act(() => {
      screen.getByText('fire-info').click();
    });
    expect(screen.getByText('Info!')).toBeInTheDocument();
  });

  it('can be dismissed manually via the close button', () => {
    render(
      <ToastProvider>
        <ToastTrigger />
      </ToastProvider>
    );
    act(() => {
      screen.getByText('fire-success').click();
    });
    expect(screen.getByText('Success!')).toBeInTheDocument();
    const dismiss = screen.getByRole('alert').querySelector('button');
    act(() => {
      dismiss.click();
    });
    expect(screen.queryByText('Success!')).toBeNull();
  });

  it('renders multiple toasts stacked', () => {
    render(
      <ToastProvider>
        <ToastTrigger />
      </ToastProvider>
    );
    act(() => {
      screen.getByText('fire-success').click();
      screen.getByText('fire-error').click();
    });
    expect(screen.getByText('Success!')).toBeInTheDocument();
    expect(screen.getByText('Error!')).toBeInTheDocument();
  });
});
