import React from 'react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ErrorBoundary from '../components/ErrorBoundary';

// A child that throws on demand so we can exercise the boundary.
function Bomb({ shouldThrow }) {
  if (shouldThrow) throw new Error('kaboom');
  return <div>Child rendered fine</div>;
}

describe('ErrorBoundary', () => {
  const originalLocation = window.location;
  const reloadMock = vi.fn();

  beforeEach(() => {
    delete window.location;
    window.location = { ...originalLocation, reload: reloadMock };
  });
  afterEach(() => {
    window.location = originalLocation;
  });

  it('renders children when no error', () => {
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={false} />
      </ErrorBoundary>
    );
    expect(screen.getByText('Child rendered fine')).toBeInTheDocument();
  });

  it('shows fallback UI when a child throws', () => {
    // Suppress the expected console.error from React.
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={true} />
      </ErrorBoundary>
    );
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByText(/kaboom/)).toBeInTheDocument();
    spy.mockRestore();
  });

  it('offers a Reload page button that reloads', async () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const user = userEvent.setup();
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={true} />
      </ErrorBoundary>
    );
    await user.click(screen.getByText('Reload page'));
    expect(reloadMock).toHaveBeenCalled();
    spy.mockRestore();
  });
});
