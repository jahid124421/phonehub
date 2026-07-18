/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#0a0e1a',
          800: '#0f1525',
          700: '#151d32',
          600: '#1c2640',
          500: '#243050',
        },
        accent: {
          blue: '#3b82f6',
          purple: '#8b5cf6',
          cyan: '#06b6d4',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        phonehub: {
          'primary': '#3b82f6',
          'secondary': '#8b5cf6',
          'accent': '#06b6d4',
          'neutral': '#1c2640',
          'base-100': '#0a0e1a',
          'base-200': '#0f1525',
          'base-300': '#151d32',
          'info': '#38bdf8',
          'success': '#4ade80',
          'warning': '#fbbf24',
          'error': '#f87171',
        },
      },
    ],
    darkTheme: 'phonehub',
  },
};
