"""Python Web API + frontend server for Render."""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"
CSS_FILE = BASE_DIR / "style.css"
JS_FILE = BASE_DIR / "app.js"

app = FastAPI(title="Python Web IDE", version="1.1.0", docs_url="/api/docs", redoc_url="/api/redoc")

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


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(INDEX_FILE, media_type="text/html")


@app.get("/style.css", include_in_schema=False)
def stylesheet() -> FileResponse:
    return FileResponse(CSS_FILE, media_type="text/css")


@app.get("/app.js", include_in_schema=False)
def javascript() -> FileResponse:
    return FileResponse(JS_FILE, media_type="application/javascript")


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    return Response(status_code=204)


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "python-web-api",
        "uptime_seconds": round(time.time() - started_at, 1),
        "frontend": True,
    }


@app.get("/api/config")
def config() -> dict[str, Any]:
    return {
        "server_execution": os.getenv("SANDBOX_EXECUTION_ENABLED", "false").lower() == "true",
        "browser_execution": True,
        "max_code_bytes": 200_000,
        "max_timeout_ms": 30_000,
    }


@app.post("/api/execute", response_model=ExecutionResponse)
def execute(_: ExecutionRequest) -> ExecutionResponse:
    if os.getenv("SANDBOX_EXECUTION_ENABLED", "false").lower() != "true":
        raise HTTPException(
            status_code=503,
            detail="Server execution is not enabled. Python currently runs in the browser.",
        )
    raise HTTPException(status_code=501, detail="Sandbox worker integration is not installed on this service.")
