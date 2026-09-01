from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.auth.providers.debug import DebugTokenVerifier
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
import os
import re
from dotenv import load_dotenv
from supabase import create_client, Client

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
if not supabase_url or not supabase_key:
    raise RuntimeError(
        "Missing SUPABASE_URL or SUPABASE_KEY. "
        "Set them in backend/.env (see .env.example) or in your environment."
    )
supabase: Client = create_client(supabase_url, supabase_key)

def validate_token(token: str) -> bool:
    # Look up your custom token in the database
        try:
            agent_res = (
                supabase.table("Agents")
                .select("user_id")
                .eq("agent_id", token)
                .limit(1)
                .execute()
            )
        except Exception:
            return False

    return bool(agent_res.data)

auth = DebugTokenVerifier(
    validate=validate_token,
    client_id="phloem-client",
    scopes=["read", "write"],
)

# Load environment variables from .env (if present)
load_dotenv()

mcp = FastMCP(name="Phloem", auth=auth)

class Data:
    sender: str
    data: str

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
            r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?\S+["\']?',
            r'(?i)(password|passwd|pwd)\s*[:=]\s*["\']?\S+["\']?',
            r'(?i)AKIA[0-9A-Z]{16}',
            r'(?i)AIza[0-9A-Za-z\\-_]{35}',
            r'(?i)[a-zA-Z0-9\\-_]+\\.[a-zA-Z0-9\\-_]+\\.[a-zA-Z0-9\\-_]+',
            r'(?i)(mongodb|postgres|mysql|sqlite)://\S+',
            r'(?i)(secret|token|key)\\s*[:=]\\s*["\']?\S+["\']?',
        ]

        for pattern in secret_patterns:
                if re.search(pattern, value):
                    return False
        return True
    
# Tool definitions
@mcp.tool()
def send_data(data: str) -> str:
    """
    Send your data to other AI Agents/Services. To use this tool, send the data to be transmitted to other agent/service.

    You'll recieve a response indicating whether the data was successfully sent or if there was an error.
    """

    raw_token = get_access_token()

    if raw_token is None:
        return "Authorization header is missing or invalid. Please provide a valid Bearer token."

    token = raw_token.token

    print(token)    # Testing purposes ONLY

    if not is_safe_data(token, "auth-token"):
        return "Authorization header contains potentially dangerous code patterns"

    if not is_safe_data(data, "data"):
        return "Data potentially contains sensitive information or secrets. Please remove any API keys, passwords, or other sensitive data before sending."

    # TODO: Validate data for malicious script injection.

    try:
        response = (
            supabase.table("Queue")
            .insert({"data": data, "sender": token})
            .execute()
        )
    except Exception as e:
        return f"Failed to send data: {e}"

    if response is None or not (200 <= getattr(response, "status_code", 0) < 300):
        return "Failed to send data: unexpected response from server"

    return "Successfully sent data to other AI Agents/Services"


@mcp.tool()
def get_data() -> Data:
    """
    Use this tool to fetch data from other AI Agents/Services
    If there's no data available, you'll receive a message indicating that no data is available.

    If data is available, you'll recieve the data, otherwise you'll receive a message indicating that no data is available.
    """

    raw_token = get_access_token()

    if raw_token is None:
        return "Authorization header is missing or invalid. Please provide a valid Bearer token."

    token = raw_token.token

    print(token)    # Testing purposes ONLY

    if not is_safe_data(token, "auth-token"):
        return "Authorization header contains potentially dangerous code patterns"

    # 1. Resolve the caller's token (agent_id) to a user_id via the Agents table
    try:
        agent_res = (
            supabase.table("Agents")
            .select("user_id")
            .eq("agent_id", token)
            .limit(1)
            .execute()
        )
    except Exception as e:
        return f"Failed to authenticate agent: {e}"

    if not agent_res.data:
        return "Unknown agent. Please provide a valid Bearer token."

    user_id = agent_res.data[0]["user_id"]

    # 2. Fetch all agent_ids belonging to that user_id
    try:
        agents_res = (
            supabase.table("Agents")
            .select("agent_id")
            .eq("user_id", user_id)
            .execute()
        )
    except Exception as e:
        return f"Failed to fetch agents for user: {e}"

    agent_ids = [row["agent_id"] for row in agents_res.data]
    if not agent_ids:
        return "No data available."

    # 3. Fetch the single latest Queue record sent by any of those agents
    try:
        queue_res = (
            supabase.table("Queue")
            .select("sender, data, created_at")
            .in_("sender", agent_ids)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
    except Exception as e:
        return f"Failed to fetch data: {e}"

    if not queue_res.data:
        return "No data available."

    record = queue_res.data[0]

    # Zero-data retention: delete the fetched record from the Queue table
    try:
        supabase.table("Queue").delete().eq("created_at", record["created_at"]).execute()
    except Exception as e:
        return f"Failed to delete delivered data: {e}"

    result = Data()
    result.sender = record["sender"]
    result.data = record["data"]

    print({result.sender, result.data})  # For debugging purposes

    return result.data # Don't return the entire Data object [FOR TESTING PURPOSES]

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ]
    )