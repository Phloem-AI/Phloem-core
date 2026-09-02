from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.main import mcp

# 1. Generate the underlying FastMCP ASGI app.
# Expose the MCP endpoint at the conventional /mcp URL.
mcp_app = mcp.http_app(
    path="/mcp",
    transport="http",
    stateless_http=True,
    json_response=True,
)

# 2. Build your primary FastAPI wrapper for Vercel.
# We map the lifespan context so initialization scripts fire reliably on cold starts.
app = FastAPI(
    title="Secure Vercel FastMCP Wrapper",
    lifespan=mcp_app.lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.mount("/", mcp_app)
