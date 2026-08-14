from fastmcp import FastMCP
from fastmcp.dependencies import CurrentHeaders
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
def send_data(headers: CurrentHeaders, data: Data) -> str:
    """
    Send your data to other AI Agents/Services. To use this tool, send a JSON body containing the 'sender' and 'data' fields.
    sender: Your name.
    data: The data to be processed by other agent/service.

    You'll recieve a response indicating whether the data was successfully sent or if there was an error.
    """
    auth = headers.get("authorization")
    if not auth:
        return "Missing Authorization header"

    scheme, _, token = auth.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return "Invalid Authorization header"

    # Validate input - don't trust user input, check for code injection
    def is_safe_data(value: str) -> bool:
        dangerous_patterns = [
            # Python patterns
            "import ", "from ", "def ", "class ", "print(", 
            # SQL patterns
            "SELECT ", "INSERT ", "UPDATE ", "DELETE ", "DROP ",
            # JavaScript patterns
            "function ", "var ", "let ", "const ", "=> ",
            # Shell patterns
            "`", "$(", ";", "|", "&",
        ]
        value_lower = value.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in value_lower:
                return False
        return True

    if not is_safe_data(token):
            return "Authorization header contains potentially dangerous code patterns"

    # TODO: Validating the data sent by AI Agent 

    # TODO: Implement your logic to send the data to other AI Agents/Services here.
    
    return "Succesfully sent data"


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