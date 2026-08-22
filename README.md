# Python Web IDE

A professional browser-based Python IDE powered by Pyodide.

## Features

- Monaco editor with Python syntax highlighting
- Multi-file local projects
- Local persistence and autosave
- Import/export projects
- Browser-based Python execution
- Lazy loading of common Pyodide packages
- Examples and command palette
- Dark/light/system theme settings
- Responsive IDE layout
- GitHub Pages compatible static deployment

## Deployment

This version requires no Render backend. Enable **Settings → Pages → Deploy from branch → main / root** in GitHub. The application is static and Python runs in the browser.

## Security model

User code is executed locally through Pyodide and is not sent to a remote Python execution server. Do not add server-side `exec()` or `eval()` for untrusted code. A future server execution provider should use isolated sandbox workers with strict CPU, memory, process, filesystem and network controls.

## Limitations

Browser Python is not identical to a Linux server. Only packages supported by the Pyodide environment are available. The Stop control stops output collection; a WebAssembly operation already running on the main thread may finish in the background.

## Future architecture

The frontend is intentionally structured so a future Render deployment can introduce an authenticated server execution provider without replacing the editor, project model or UI.
