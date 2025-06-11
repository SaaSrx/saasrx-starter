# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a SaaS starter application built with **Reflex** (v0.7.x), a full-stack Python web framework. The project uses a monorepo structure with uv workspaces and includes authentication, payments (Stripe), email capabilities, and an admin interface.

## Development Commands

```bash
# Install dependencies
uv sync

# Install custom rxext package (required)
pip install -e ./packages/rxext

# Install admin dashboard dependency (required separately)
pip install starlette-admin

# Start development server
reflex run

# Enable debugging (when needed)
REFLEX_USE_GRANIAN=0 reflex run

# Run tests
pytest
```

## Architecture

**Core Pattern**: Full-stack Python using Reflex's component-based architecture
- Frontend: React-like components written in Python (saasrx/pages/)
- Backend: FastAPI integration for API routes (saasrx/api/)
- State: Centralized state management using Reflex State classes (saasrx/state/)
- Components: Reusable components in rxext workspace package

**Key Routes:**
- `/`: Main application index
- `/admin`: Admin dashboard (localhost:8000/admin in dev)
- `/api/v1/health`: API health check endpoint
- `/auth/verify`: Authentication verification
- `/dashboard`: User dashboard

## Configuration

**Environment Variables**: Use mise for environment management (preferred over rxconfig.toml)
- `.mise.test.toml` for test environment
- `.mise.prod.toml` for production environment

**Database**: PostgreSQL with Reflex Models/SQLAlchemy integration

## Important Notes

- Project is currently in refactoring phase migrating to Reflex 0.7.x
- Use `uv` for all package management (not pip) for better workspace compatibility
- Admin dashboard requires separate starlette-admin installation
- Debugging requires `REFLEX_USE_GRANIAN=0` environment variable