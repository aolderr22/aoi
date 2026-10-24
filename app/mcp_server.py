import json
import os
import httpx
from mcp.server import MCPServer

mcp = MCPServer("AOI Character Server")

API_BASE_URL = os.getenv(
    "AOI_API_BASE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

@mcp.tool()
def list_characters() -> str:
    """Retrieve character records from the AOI FastAPI endpoint."""

    url = f"{API_BASE_URL}/characters"

    try:
        response = httpx.get(url, timeout=20.0)
        response.raise_for_status()
        return json.dumps(
            response.json(),
            ensure_ascii=False,
            indent=2,
        )
    except httpx.HTTPError as exc:
        raise RuntimeError(
            f"Could not retrieve characters from FastAPI: {exc}"
        ) from exc

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
    )