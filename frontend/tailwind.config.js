/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#7C3AED",
        secondary: "#A78BFA",
        accent: "#0891B2",
        background: "#FAF5FF",
        foreground: "#1E1B4B",
        card: "#FFFFFF",
        muted: "#ECEEF9",
        "muted-foreground": "#475569",
        border: "#DDD6FE",
        destructive: "#DC2626",
        ring: "#7C3AED",
      }
    },
  },
  plugins: [],
}
