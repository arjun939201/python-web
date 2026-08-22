# Python Web IDE

A professional browser-based Python IDE powered by Pyodide. Python executes locally in the browser; there is no server-side code execution in this version.

## Features

- Monaco editor
- Multi-file local projects
- Local autosave and persistence
- Import/export projects
- Python execution with Pyodide
- Lazy loading of common Pyodide packages
- Examples
- Command palette
- Settings and themes
- Responsive IDE layout
- GitHub Pages compatible

## GitHub Pages

Enable **Settings → Pages → Deploy from branch → main / root** in the repository. The app is static and does not require Render.

## Limitations

Browser execution is different from a server compiler. Not every PyPI package is available, execution cannot access your server filesystem, and the Stop control can only stop output collection for work already running in WebAssembly.

## Future architecture

The frontend is structured around an execution service boundary so a future Render deployment can add authenticated server execution through isolated sandbox workers without exposing `exec()` on the web server.
