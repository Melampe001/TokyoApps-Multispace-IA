# PWA Template

This template generates a Progressive Web App using React and Vite.

## Features

- React 18+
- Vite for fast development
- Service Worker for offline support
- Responsive design ready
- TypeScript support

## Structure

```
pwa-project/
├── src/
│   ├── components/   # Reusable components
│   ├── pages/        # Page components
│   ├── styles/       # CSS/styling
│   ├── utils/        # Utility functions
│   ├── App.jsx       # Main app component
│   └── main.jsx      # Entry point
├── public/           # Static assets
├── tests/
│   ├── unit/         # Unit tests
│   └── e2e/          # End-to-end tests
└── deploy/           # Deployment configs
```

## Generated Files

- `package.json` - Dependencies and scripts
- `vite.config.js` - Vite configuration
- `index.html` - HTML entry point
- `Dockerfile` - Container definition
- `.github/workflows/ci.yml` - CI/CD pipeline

## Next Steps

1. Install dependencies: `npm install`
2. Start dev server: `npm run dev`
3. Run tests: `npm test`
4. Build for production: `npm run build`
