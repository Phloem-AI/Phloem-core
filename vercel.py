from fastapi import FastAPI
from backend.main import mcp

# 1. Extract the underlying FastMCP ASGI instance
mcp_app = mcp.http_app()

# 2. Feed FastMCP's lifecycle array strictly to a root FastAPI instance
app = FastAPI(
    title="Vercel FastMCP Wrapper",
    lifespan=mcp_app.lifespan,  # Ensures startup routines execute safely
    routes=mcp_app.routes       # Maps the underlying JSON-RPC MCP routes
)
