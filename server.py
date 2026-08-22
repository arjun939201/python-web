"""Render-ready API foundation.

This service intentionally does NOT execute arbitrary Python source on the Render
web process. Running untrusted code directly with subprocess/exec on a normal web
service is unsafe. A future sandbox worker should implement ExecutionProvider behind
an isolated container/VM boundary with CPU, memory, process, filesystem and network
limits.
"""
from __future__ import annotations

import os
import time
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Python Web API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
origins = [x.strip() for x in frontend_origin.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=frontend_origin != "*",
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

started_at = time.time()


class ExecutionRequest(BaseModel):
    code: str = Field(min_length=0, max_length=200_000)
    stdin: str = Field(default="", max_length=20_000)
    timeout_ms: int = Field(default=5_000, ge=250, le=30_000)


class ExecutionResponse(BaseModel):
    status: str
    message: str
    provider: str


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "python-web-api",
        "uptime_seconds": round(time.time() - started_at, 1),
    }


@app.get("/api/config")
def config() -> dict[str, Any]:
    """Public capability discovery; no secrets are returned."""
    return {
        "server_execution": os.getenv("SANDBOX_EXECUTION_ENABLED", "false").lower() == "true",
        "browser_execution": True,
        "max_code_bytes": 200_000,
        "max_timeout_ms": 30_000,
    }


@app.post("/api/execute", response_model=ExecutionResponse)
def execute(_: ExecutionRequest) -> ExecutionResponse:
    """Explicitly refuse unsafe direct server execution.

    This endpoint becomes active only after an isolated sandbox worker is wired in.
    """
    if os.getenv("SANDBOX_EXECUTION_ENABLED", "false").lower() != "true":
        raise HTTPException(
            status_code=503,
            detail=(
                "Server execution is not enabled. Python currently runs in the browser. "
                "Configure an isolated sandbox worker before enabling this endpoint."
            ),
        )
    raise HTTPException(
        status_code=501,
        detail="Sandbox worker integration is not installed on this service.",
    )
