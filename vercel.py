from backend.main import mcp

# FastMCP's http_app is the ASGI application
app = mcp.http_app()

# This is the ASGI application that Vercel will use