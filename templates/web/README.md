# PWA Template

Production-ready Progressive Web App template with React, Vite, TypeScript, and offline support.

## Features

- ✅ React 18 with TypeScript
- ✅ Vite for fast builds
- ✅ PWA with offline support
- ✅ Service Worker
- ✅ App manifest
- ✅ Responsive design
- ✅ Tailwind CSS
- ✅ React Router
- ✅ State management (Zustand/Redux)
- ✅ API integration (Axios)
- ✅ Form handling (React Hook Form)
- ✅ Testing (Vitest + React Testing Library)
- ✅ Lighthouse score > 90

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
web-template/
├── public/
│   ├── manifest.json         # PWA manifest
│   ├── icons/                # App icons
│   └── robots.txt
├── src/
│   ├── components/           # React components
│   │   ├── common/
│   │   ├── layout/
│   │   └── features/
│   ├── pages/                # Page components
│   │   ├── Home.tsx
│   │   ├── About.tsx
│   │   └── NotFound.tsx
│   ├── hooks/                # Custom hooks
│   ├── utils/                # Utilities
│   ├── services/             # API services
│   ├── store/                # State management
│   ├── styles/               # Global styles
│   ├── types/                # TypeScript types
│   ├── App.tsx               # Main app (see App.tsx.txt)
│   ├── main.tsx              # Entry point
│   └── service-worker.ts     # Service worker
├── tests/                    # Tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── index.html
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

> **Note:** See `App.tsx.txt` in this directory for a sample implementation.

## PWA Features

### Manifest

App manifest for installability:

```json
{
  "name": "My PWA",
  "short_name": "PWA",
  "theme_color": "#000000",
  "background_color": "#ffffff",
  "display": "standalone",
  "orientation": "portrait",
  "scope": "/",
  "start_url": "/",
  "icons": [
    {
      "src": "icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### Service Worker

Offline support with caching:

```typescript
// Cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('v1').then((cache) => {
      return cache.addAll([
        '/',
        '/index.html',
        '/src/main.tsx',
        '/src/App.tsx'
      ]);
    })
  );
});

// Serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

## Development

### Hot Reload

Vite provides instant hot module replacement:

```bash
npm run dev
```

### Type Checking

TypeScript for type safety:

```bash
npm run type-check
```

### Linting

ESLint for code quality:

```bash
npm run lint
npm run lint:fix
```

### Testing

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

## Building

### Production Build

```bash
npm run build
```

Output in `dist/` directory.

### Preview Build

```bash
npm run preview
```

Preview production build locally.

## Deployment

### Vercel

```bash
vercel deploy
```

### Netlify

```bash
netlify deploy --prod
```

### Docker

```bash
docker build -t pwa-template .
docker run -p 3000:3000 pwa-template
```

## Performance Optimization

- Code splitting
- Lazy loading routes
- Image optimization
- Compression (Gzip/Brotli)
- Caching strategy
- Tree shaking
- Minification

## Responsive Design

- Mobile-first approach
- Tailwind CSS utilities
- Breakpoints: sm, md, lg, xl, 2xl
- Flexbox and Grid layouts
- Touch-friendly targets

## State Management

### Zustand Example

```typescript
import { create } from 'zustand';

interface Store {
  count: number;
  increment: () => void;
  decrement: () => void;
}

export const useStore = create<Store>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));
```

## API Integration

### Axios Service

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

## Environment Variables

```bash
# .env.local
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My PWA
VITE_ENABLE_ANALYTICS=true
```

Access in code:

```typescript
const apiUrl = import.meta.env.VITE_API_URL;
```

## Testing

### Unit Tests

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

test('renders button', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByText('Click me')).toBeInTheDocument();
});
```

### E2E Tests

```typescript
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

## Lighthouse Scores

Target scores:
- Performance: > 90
- Accessibility: > 90
- Best Practices: > 90
- SEO: > 90
- PWA: ✓

## License

MIT License

---

Generated with Tokyo-IA Elite Framework
