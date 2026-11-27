"""Private Task Bridge scaffold. Do not deploy publicly without authentication."""
import os
from datetime import datetime, timezone
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="VATHEN Task Bridge", version="0.1.0")

class TaskUpdate(BaseModel):
    task_id: str = Field(min_length=1, max_length=200)
    status: str = Field(pattern="^(Not started|In progress|Done|Blocked)$")
    evidence: str = Field(min_length=8, max_length=4000)

@app.get("/health")
def health():
    return {"status": "scaffold", "utc": datetime.now(timezone.utc).isoformat(), "notion_configured": bool(os.getenv("NOTION_TOKEN"))}

@app.post("/tasks/update")
def update_task(payload: TaskUpdate, authorization: str | None = Header(default=None)):
    expected = os.getenv("TASK_BRIDGE_API_KEY")
    if not expected:
        raise HTTPException(status_code=503, detail="Task Bridge is not configured for authenticated operation")
    if authorization != f"Bearer {expected}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Deliberately no Notion mutation until database IDs, property mapping,
    # idempotency, audit persistence and least-privilege scopes are configured.
    raise HTTPException(status_code=501, detail="Notion adapter is intentionally not enabled in this scaffold")
