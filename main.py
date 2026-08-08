from starlette.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from starlette.middleware import Middleware
from dotenv import load_dotenv

load_dotenv()
mcp = FastMCP(name="Phloem")

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ]
    )