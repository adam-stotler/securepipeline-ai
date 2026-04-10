"""
SecurePipeline.ai — FastAPI entry point.
Placeholder for Phase 1. API routes built in Phase 4.
"""
from fastapi import FastAPI

app = FastAPI(title="SecurePipeline.ai", version="0.1.0")


@app.get("/health")
def health_check() -> dict:
    """Liveness probe — used by container orchestration and pipeline smoke tests."""
    return {"status": "ok", "service": "securepipeline-ai"}
