import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the mcp instance from main
from main import mcp

# Create the ASGI app by calling http_app() as a method
app = mcp.http_app()

# This is the ASGI application that Vercel will use