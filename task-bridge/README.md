# VATHEN Task Bridge (scaffold)

This FastAPI service is deliberately non-production. GitHub Pages cannot host it; deploy only to a private service after security review.

## Local checks

```bash
pip install -r requirements.txt
PYTHONPATH=. pytest -q
uvicorn app.main:app --reload
```

## Before production
- Configure a server-side Notion integration with minimum required permissions.
- Set `NOTION_TOKEN`, `TASK_BRIDGE_API_KEY`, and explicit database/property IDs via secret management.
- Implement authentication/SSO, authorization, durable audit logs, idempotency, concurrency control, retries, rate limits, monitoring and rollback.
- Validate task completion evidence before writing status.
- Never expose secrets in browser code, Git history, logs, or public issues.
