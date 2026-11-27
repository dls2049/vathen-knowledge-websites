# VATHEN Knowledge Websites

V2.3.2 — public navigation shell for the VATHEN Agent Knowledge Hub and Knowledge Library.

## Sites
- `/` — portal
- `/knowledge-hub/` — Agent Knowledge Hub and engineering overview
- `/knowledge-library/` — ten-domain knowledge library navigation

## Architecture
The static GitHub Pages site is a navigation and read-only status surface. Notion remains the source of truth for knowledge pages and task records. No Notion credentials or private data belong in this repository.

The `task-bridge/` directory is a separate FastAPI scaffold. It is not deployed by GitHub Pages and must be hosted privately with authentication and server-side secrets before connecting to Notion.

## Deploy
GitHub Actions deploys the repository root to GitHub Pages on pushes to `main`. Enable Pages with **GitHub Actions** as the build and deployment source if it is not already enabled.

## Safety
Never place API tokens, `.env` files, personal information, or private Notion exports in this public repository.
