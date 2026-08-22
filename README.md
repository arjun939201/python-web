# Python Web IDE

A professional browser-based Python IDE powered by Pyodide, with a Render-ready API foundation for a future isolated execution service.

## What works today

- Monaco editor with Python syntax highlighting
- Multi-file local projects
- Local persistence and autosave
- Import/export projects
- Browser-based Python execution
- Lazy loading of common Pyodide packages
- Examples and command palette
- Dark/light/system theme settings
- Responsive IDE layout
- GitHub Pages static deployment
- Render-ready FastAPI health/config endpoints

## Architecture

```text
GitHub Pages
    |
    v
Python Web IDE
    |
    +--> BrowserPythonProvider (Pyodide)  <-- current execution path
    |
    +--> ServerPythonProvider (future)
              |
              v
        Render API /api/execute
              |
              v
       Isolated sandbox worker
```

The Render API deliberately refuses to execute arbitrary Python directly. A normal web process must never run untrusted source with `exec()`, `eval()`, or an unrestricted subprocess. The safe server architecture requires an isolated worker boundary with CPU, memory, process, filesystem, timeout and network controls.

## GitHub Pages deployment

The static IDE can run without Render. The repository includes a GitHub Actions Pages workflow. Enable **Settings → Pages → Source: GitHub Actions** and pushes to `main` deploy the site.

Expected URL:

`https://arjun939201.github.io/python-web/`

## Render API deployment

`render.yaml` defines a Python web service.

1. In Render, create a new Blueprint from this repository, or create a Python web service manually.
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
4. Health check: `/api/health`
5. Keep `SANDBOX_EXECUTION_ENABLED=false` until a real isolated sandbox worker is connected.
6. Set `FRONTEND_ORIGIN` to the deployed frontend origin.

Useful endpoints:

- `GET /api/health`
- `GET /api/config`
- `POST /api/execute` — intentionally returns `503` until a sandbox worker is installed
- `/api/docs` — FastAPI API documentation

## Security model

Current Python execution is local through Pyodide. Code is not sent to the Render API for execution.

When server execution is introduced, use a dedicated isolated worker or third-party sandbox. The worker should have:

- non-root execution
- CPU and memory quotas
- strict wall-clock timeout
- process/file descriptor limits
- isolated temporary filesystem
- disabled or tightly controlled network access
- no access to application secrets
- rate limiting and authenticated job ownership
- bounded stdout/stderr
- a queue so web processes never execute user code

Never expose API keys in frontend code.

## Browser limitations

Browser Python is not identical to a Linux server. Only packages supported by the Pyodide environment are available. The current Stop control stops output collection; a WebAssembly operation already running may finish in the background.

## Roadmap

1. Add an authenticated project API backed by a real database.
2. Add a sandbox provider using an isolated worker/third-party execution service.
3. Add job queues, quotas, cancellation and streaming output.
4. Add cloud project sync and sharing.
5. Add GitHub integration and collaborative editing.

## Local development

The static app can be served by any static HTTP server. The optional API can be started with:

```bash
pip install -r requirements.txt
uvicorn server:app --reload
```

The frontend remains usable without the API.
