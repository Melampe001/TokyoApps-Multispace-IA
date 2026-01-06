# Tokyo IA Web Dashboard

Web interface for Tokyo IA - AI Agent Orchestration Platform.

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Environment Variables

Create a `.env` file in the `web/` directory based on `.env.example`:

```bash
cp .env.example .env
```

### Required Variables

- `VITE_API_BASE_URL` - Base URL for the Tokyo IA API (default: http://localhost:8080)
- `VITE_API_TIMEOUT` - API request timeout in milliseconds (default: 10000)

### Optional Variables

- `VITE_ENABLE_ADMIN_PANEL` - Enable/disable admin panel features (default: true)
- `VITE_ENABLE_ANALYTICS` - Enable/disable analytics tracking (default: false)
- `VITE_SENTRY_DSN` - Sentry DSN for error tracking
- `VITE_GA_TRACKING_ID` - Google Analytics tracking ID

**Note:** All environment variables for Vite must be prefixed with `VITE_` to be exposed to the client-side code.

## Features

- 🎨 Modern React 18 application
- ⚡ Fast development with Vite
- 🛣️ Client-side routing with React Router DOM
- 📡 API integration with Axios
- 🎛️ Admin panel for agent management
- 📱 Responsive design

## Project Structure

```
web/
├── src/
│   ├── components/       # React components
│   │   └── AdminPanel.jsx
│   ├── routes/          # Route definitions
│   │   └── index.jsx
│   ├── App.jsx          # Main app component
│   ├── App.css          # App styles
│   ├── main.jsx         # Application entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── package.json         # Dependencies and scripts
└── .env.example         # Environment variables template
```

## Deployment

This app is automatically deployed to Vercel on push to main branch.

### Manual Deployment

```bash
# Build the application
npm run build

# Deploy to Vercel
vercel --prod
```

## Technology Stack

- React 18
- Vite
- React Router DOM
- Axios
- Modern CSS

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

