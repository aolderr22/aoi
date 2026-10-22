import json
import httpx
from mcp.server import MCPServer

mcp = MCPServer("AOI Character Server")

@mcp.tool()
def list_characters() -> str:
    """List all characters available from the AOI character API."""

    try:
        response = httpx.get(
            "http://127.0.0.1:8000/characters",
            timeout=15.0,
        )
        response.raise_for_status()

        return json.dumps(
            response.json(),
            ensure_ascii=False,
            indent=2,
        )

    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Could not retrieve characters from the FastAPI service."
        ) from exc


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
    )
