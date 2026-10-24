import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_URL = "http://127.0.0.1:8001/mcp"

async def main():
    async with streamable_http_client(MCP_URL) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Discover available MCP tools.
            tools_result = await session.list_tools()

            print("Available MCP tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")

            # Test list_employees.
            print("\n--- Testing list_employees ---")
            employees_result = await session.call_tool(
                "list_employees",
                {},
            )

            for content in employees_result.content:
                if hasattr(content, "text"):
                    print(content.text)

            if employees_result.is_error:
                print("The list_employees tool reported an error.")

            # Test recommend_employee.
            print("\n--- Testing recommend_employee ---")
            recommendation_result = await session.call_tool(
                "recommend_employee",
                {
                    "task": (
                        "Build a Python API that queries SQL data "
                        "and deploys infrastructure using Pulumi."
                    )
                },
            )

            for content in recommendation_result.content:
                if hasattr(content, "text"):
                    print(content.text)

            if recommendation_result.is_error:
                print("The recommend_employee tool reported an error.")

if __name__ == "__main__":
    asyncio.run(main())