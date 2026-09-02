from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.main import mcp

# 1. Generate the underlying FastMCP ASGI app.
# By setting path="/", the MCP handlers operate cleanly at the root URL.
mcp_app = mcp.http_app(path="/")

# 2. Build your primary FastAPI wrapper for Vercel.
# We map the lifespan context so initialization scripts fire reliably on cold starts.
app = FastAPI(
    title="Secure Vercel FastMCP Wrapper",
    lifespan=mcp_app.lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", mcp_app)
