# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project Overview

**Phloem-core** is a multi-vendor AI agent interoperability layer built around a secure MCP (Model Context Protocol) server. It lets one AI agent hand work to another with explicit semantics, policy enforcement, and auditability — an "MCP-native semantic context firewall" for cross-vendor agent handoffs.

It is **not**: a generic MCP proxy, an orchestration platform, or an agent marketplace.

## Repository Structure

```
Phloem-core/
├── backend/
│   ├── main.py            # MCP tools, authentication, and Supabase access
│   └── .env.example       # Template for required environment variables
├── vercel.py              # Vercel ASGI entrypoint; serves MCP at /mcp
├── vercel.json            # Vercel Python build and catch-all route
├── requirements.txt       # Python dependencies (repository root)
├── README.md              # Product vision and local setup guide
├── CONTRIBUTING.md
└── LICENSE                # Apache-2.0
```

## Tech Stack

- **Python 3.12+**
- **FastMCP** (`fastmcp`) — MCP server framework; tools defined via `@mcp.tool()` decorators
- **Starlette middleware** — CORS configuration on the HTTP transport
- **Supabase** (`supabase-py`) — storage/backend-as-a-service client

## Setup & Run

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Create `backend/.env` (see `backend/.env.example`):

```
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_KEY=your-supabase-key
```

Run the server:

```powershell
python backend/main.py
```

The local server runs over HTTP at `0.0.0.0:8000`. The Vercel ASGI entrypoint is
`vercel.py`, and the deployed MCP endpoint is `/mcp`.

## Architecture Notes

- The server exposes two MCP tools:
  - `send_data(data)` — obtains the bearer token from FastMCP request context,
    validates it against `Agents.agent_id`, screens the payload, and inserts it
    into `Queue`.
  - `get_data()` — obtains the bearer token, finds agents for the same user,
    returns the latest matching queue record, and then deletes that record.
- Auth model: **UUID API keys** passed as bearer tokens.
- The Vercel transport uses stateless Streamable HTTP with JSON responses so
  requests do not depend on one serverless instance.
- Supabase client is initialized at module load from `SUPABASE_URL` and
  `SUPABASE_KEY`.
- Secret handling currently rejects several detected patterns; it does not
  extract or redact secrets.

## Conventions for Agents

- Keep changes focused on the owning file. Deployment behavior belongs in
  `vercel.py` and `vercel.json`; MCP and data behavior belongs in
  `backend/main.py`.
- Never commit `.env`, API keys, or tokens. Use `.env.example` as the template.
- Don't introduce unnecessary dependencies that can be avoided with simple work-arounds.
- Preserve the security posture: validate all incoming headers and payloads; treat all input as untrusted.
- Test the code after any changes are made.
- Match existing style: plain functions, docstrings written as tool descriptions for LLM consumers, inline `# TODO:` comments for unfinished work.
- Update `README.md` / `TODO` when adding features that change scope.

## Deployment Safety

The Vercel entrypoint serves `/mcp` and is configured for stateless JSON HTTP.
Before production deployment, verify all of the following:

- Configure `SUPABASE_URL` and `SUPABASE_KEY` in Vercel project environment
  variables for every intended deployment environment. Never expose a service
  key to browser code.
- Use a least-privilege Supabase key and enforce tenant isolation with database
  policies. The current server-side key can bypass RLS if it is a service key.

This project is deployed on Vercel Serverless.
