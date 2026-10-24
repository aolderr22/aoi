import json
import os
import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("AOI Employee Server")

API_BASE_URL = os.getenv(
    "AOI_API_BASE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

@mcp.tool()
def list_employees() -> str:
    """Retrieve employee records from the AOI FastAPI endpoint."""
    response = httpx.get(
        f"{API_BASE_URL}/employees",
        timeout=20.0,
    )
    response.raise_for_status()

    return json.dumps(response.json(), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
    )