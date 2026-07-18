import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://jahid124421.github.io',
  base: '/phonehub',
  output: 'static',
  integrations: [
    tailwind(),
    sitemap(),
  ],
  build: {
    format: 'directory',
  },
});
