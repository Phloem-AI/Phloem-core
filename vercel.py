from fastapi import FastAPI
from backend.main import mcp

# 1. Extract the underlying FastMCP ASGI instance
mcp_app = mcp.http_app()

# 2. Feed FastMCP's lifecycle array strictly to a root FastAPI instance
app = FastAPI(
    title="Vercel FastMCP Wrapper",
    lifespan=mcp_app.lifespan  # Ensures startup routines execute safely     
)

# 3. Safely mount FastMCP to handle ALL traffic at the root URL
app.mount("/", mcp_app)