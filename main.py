from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP(name="Phloem")

class Data:
    """Data class for the tool"""
    sender: str
    data: str

@mcp.tool()
def send_data(data: Data) -> str:
    """
    Send your data to other AI Agents/Services. To use this tool, send a JSON body containing the 'sender' and 'data' fields.
    sender: Your API authentication key for Phloem MCP.
    data: The data to be processed by the target agent.
    """
    return "Data: " + data


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