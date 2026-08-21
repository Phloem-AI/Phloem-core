# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project Overview

**Phloem-core** is a multi-vendor AI agent interoperability layer built around a secure MCP (Model Context Protocol) server. It lets one AI agent hand work to another with explicit semantics, policy enforcement, and auditability — an "MCP-native semantic context firewall" for cross-vendor agent handoffs.

It is **not**: a generic MCP proxy, an orchestration platform, or an agent marketplace.

## Repository Structure

```
Phloem-core/
├── backend/
│   ├── main.py            # Entire MCP server (single-file app)
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Template for required env vars
├── README.md              # Product vision + local setup guide
├── CONTRIBUTING.md
└── LICENSE                # Apache-2.0
```

## Tech Stack

- **Python 3.12+**
- **FastMCP** (`fastmcp`) — MCP server framework; tools defined via `@mcp.tool()` decorators
- **Starlette middleware** — CORS configuration on the HTTP transport
- **Supabase** (`supabase-py`) — storage/backend-as-a-service client

## Setup & Run

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows; `source venv/bin/activate` on Unix
pip install -r requirements.txt
```

Create `backend/.env` (see `.env.example`):

```
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_PUBLISHABLE_KEY=your-supabase-key
```

Run the server:

```powershell
python main.py
```

The server runs over HTTP transport at `0.0.0.0:8000` with permissive CORS.

## Architecture Notes

- The server exposes two MCP tools:
  - `send_data(headers, data)` — receives `{sender, data}` from an agent, validates the `Authorization: Bearer <token>` header, screens for code-injection patterns and secret leakage, then relays the data.
  - `get_data(headers)` — fetches pending data for the calling agent (not yet implemented).
- Auth model: **UUID API keys** passed as bearer tokens.
- Design goals: zero-data retention (data deleted once delivered), secret extraction/redaction, policy-driven handoffs.
- Supabase client is initialized at module load from env vars.

## Known TODOs / Incomplete Areas

- `send_data`: validation of `data.data` for malicious content/injection is still a TODO; actual relay logic to destination agents is unimplemented.
- `get_data`: entirely unimplemented (`pass`); queue behavior using `created_at()` timestamps is planned.
- Env vars are read via `os.getenv` but `.env` loading may need `python-dotenv` or similar — verify before assuming values are present.

## Conventions for Agents

- Keep changes within `backend/`; this is currently a single-file server.
- Never commit `.env`, API keys, or tokens. Use `.env.example` as the template.
- Preserve the security posture: validate all incoming headers and payloads; treat all input as untrusted.
- Match existing style: plain functions, docstrings written as tool descriptions for LLM consumers, inline `# TODO:` comments for unfinished work.
- Update `README.md` / `TODO` when adding features that change scope.
