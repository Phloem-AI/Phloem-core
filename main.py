from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP(name="Phloem")

class Data:
    """Data class for the tool"""
    model: str
    data: str

@mcp.tool()
def get_my_todos(data: Data) -> str:
    """
    Send your data to other AI Agents/Services. To use this tool, send a JSON body containing the 'model' and 'data' fields.
    Model: The model to use for processing the data (e.g., "gpt-4", "gpt-3.5-turbo").
    Data: The data to be processed by the specified model.
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