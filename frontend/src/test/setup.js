// Vitest global setup: brings in jest-dom matchers and polyfills as needed.
import '@testing-library/jest-dom/vitest';

// jsdom doesn't implement matchMedia, which some components may query.
if (!window.matchMedia) {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: (query) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: () => {},
      removeListener: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => false,
    }),
  });
}

// jsdom doesn't implement ResizeObserver; recharts needs it to render.
if (!window.ResizeObserver) {
  window.ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
}

// Stub IntersectionObserver similarly.
if (!window.IntersectionObserver) {
  window.IntersectionObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
    takeRecords() {
      return [];
    }
  };
}

// scrollTo isn't implemented in jsdom; silently no-op to avoid errors.
if (!window.scrollTo) {
  window.scrollTo = () => {};
}
