from app.mcp.registry import ToolRegistry

class MCPClient:
    """
    Executes tools registered with the MCP tool registry.

    This is an abstraction layer between the agent
    and available application capabilities.
    """

    def __init__(
        self,
        registry: ToolRegistry,
    ):
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        **kwargs,
    ):
        """
        Execute a registered tool.
        """

        tool = self.registry.get_tool(
            tool_name
        )

        if tool is None:
            raise ValueError(
                f"Tool '{tool_name}' does not exist."
            )

        function = tool["function"]

        return function(
            **kwargs
        )

    def available_tools(self) -> list[dict]:
        """
        Return tools available to the agent.
        """

        return self.registry.list_tools()