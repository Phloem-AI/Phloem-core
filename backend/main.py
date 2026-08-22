from fastmcp import FastMCP
from fastmcp.dependencies import CurrentHeaders
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
import os
import re
from supabase import create_client, Client


mcp = FastMCP(name="Phloem")

class Data:
    """Data class for the tool"""
    sender: str
    data: str

# Initialize Supabase client
supabase: Client = None
supabase_url = os.getenv("SUPABASE_URL")    
supabase_key = os.getenv("SUPABASE_PUBLISHABLE_KEY")  
supabase = create_client(supabase_url, supabase_key)

#Utility functions
def is_safe_data(value: str, type: str) -> bool:

    if type == "auth-token":

        dangerous_patterns = [
            "import ", "from ", "def ", "class ", "print(", 
            "SELECT ", "INSERT ", "UPDATE ", "DELETE ", "DROP ",
            "function ", "var ", "let ", "const ", "=> ",
            "`", "$(", ";", "|", "&",
        ]
        
        value_lower = value.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in value_lower:
                return False
        return True 
    elif type == "data":

        secret_patterns = [
            # API keys (various formats)
            r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?\S+["\']?',
            # Passwords
            r'(?i)(password|passwd|pwd)\s*[:=]\s*["\']?\S+["\']?',
            # AWS keys
            r'(?i)AKIA[0-9A-Z]{16}',
            # Google API keys
            r'(?i)AIza[0-9A-Za-z\\-_]{35}',
            # JWT tokens (already validated in auth, but check for leakage)
            r'(?i)[a-zA-Z0-9\\-_]+\\.[a-zA-Z0-9\\-_]+\\.[a-zA-Z0-9\\-_]+',
            # Database connection strings
            r'(?i)(mongodb|postgres|mysql|sqlite)://\S+',
            # Generic secret patterns
            r'(?i)(secret|token|key)\\s*[:=]\\s*["\']?\S+["\']?',
        ]

        for pattern in secret_patterns:
                if re.search(pattern, value):
                    return False
        return True
    
# Tool definitions
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
    if not is_safe_data(token, "auth-token"):
        return "Authorization header contains potentially dangerous code patterns"

    data_value = data.data

    # Detect potential secret leakage using regex patterns
    if not is_safe_data(data_value, "data"):
        return "Data potentially contains sensitive information or secrets. Please remove any API keys, passwords, or other sensitive data before sending."

    # TODO: Validate data.data for malicious script injection.

    # Send the data to Supabase (Queue table) for relaying to other AI Agents/Services
    try:
        response = (
            supabase.table("Queue")
            .insert({"data": data_value, "sender": token})
            .execute()
        )
    except Exception as e:
        return f"Failed to send data: {e}"

    # Supabase returns 201 on successful insert; treat any 2xx as success
    if response is None or not (200 <= getattr(response, "status_code", 0) < 300):
        return "Failed to send data: unexpected response from storage"

    return "Success"


@mcp.tool()
def get_data(headers: CurrentHeaders) -> Data:
    """
    Use this tool to fetch data from other AI Agents/Services
    If there's no data available, you'll receive a message indicating that no data is available.

    If data is available, you'll recieve a JSON body with these fields of data:
    sender: The name of the sender.
    data: The data sent by the sender.
    """
    # TODO: Implement your logic to fetch data here (Oldest data first).

    pass

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