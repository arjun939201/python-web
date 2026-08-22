# Python Runner

A lightweight browser-based Python playground powered by [Pyodide](https://pyodide.org/).

## Features

- Run Python 3 directly in the browser
- No Python backend required
- Standard output and error capture
- Run/stop controls
- Example programs
- Keyboard shortcut: `Ctrl/Cmd + Enter`
- Dark/light theme
- Responsive layout

## Run locally

Because Pyodide is loaded from a CDN, serve the project over HTTP rather than opening `index.html` directly:

```bash
python -m http.server 8080
```

Then open <http://localhost:8080>.

## Deploy

This is a static site and can be deployed to GitHub Pages, Netlify, Vercel, Cloudflare Pages, or any static hosting service.

### GitHub Pages

1. Open **Settings → Pages** in this repository.
2. Select **Deploy from a branch**.
3. Select `main` and `/ (root)`.
4. Save and wait for the deployment.

## Architecture

The browser downloads Pyodide (Python compiled to WebAssembly) and executes submitted code locally. User code is not sent to a custom execution server.

This makes the MVP inexpensive and avoids exposing a server-side Python interpreter to arbitrary internet users. For server-side execution, add isolated workers with strong sandboxing, resource limits, and a queue before accepting untrusted public code.
