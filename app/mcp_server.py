import json
import httpx
from mcp.server import MCPServer

mcp = MCPServer("AOI Character Server")
FASTAPI_CHARACTERS_URL = "http://127.0.0.1:8000/characters"

@mcp.tool()
def list_characters() -> str:
    """Retrieve all characters from the AOI character API."""

    response = httpx.get(
        FASTAPI_CHARACTERS_URL,
        timeout=20.0,
    )
    response.raise_for_status()

    return json.dumps(
        response.json(),
        ensure_ascii=False,
        indent=2,
    )

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
    )