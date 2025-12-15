# E-commerce Template

This template generates a full-featured e-commerce platform using Next.js.

## Features

- Next.js 14+ with App Router
- Stripe payment integration
- Prisma ORM
- PostgreSQL database
- TypeScript
- TailwindCSS for styling
- Admin panel structure

## Structure

```
ecommerce-project/
├── app/
│   ├── (auth)/       # Authentication pages
│   ├── (shop)/       # Shop pages
│   └── admin/        # Admin panel
├── components/
│   └── ui/           # UI components
├── lib/              # Utilities and helpers
├── api/              # API routes
├── prisma/           # Database schema
├── tests/
│   ├── unit/         # Unit tests
│   └── e2e/          # End-to-end tests
└── deploy/           # Deployment configs
```

## Generated Files

- `package.json` - Dependencies and scripts
- `app/page.tsx` - Home page
- `prisma/schema.prisma` - Database schema
- `.env.example` - Environment variables
- `Dockerfile` - Container definition
- `.github/workflows/ci.yml` - CI/CD pipeline

## Next Steps

1. Copy `.env.example` to `.env` and configure
2. Install dependencies: `npm install`
3. Setup database: `npx prisma migrate dev`
4. Start dev server: `npm run dev`
5. Access store: `http://localhost:3000`
