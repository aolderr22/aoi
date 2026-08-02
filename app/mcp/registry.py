from typing import Callable

class ToolRegistry:
    """
    Stores tools available to the AI agent.

    MCP tools are registered here and exposed
    to the LLM layer.
    """

    def __init__(self):
        self.tools: dict[str, Callable] = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable,
    ) -> None:
        """
        Register a new tool.
        """

        self.tools[name] = {
            "description": description,
            "function": function,
        }

    def get_tool(
        self,
        name: str,
    ):
        """
        Retrieve a tool by name.
        """

        return self.tools.get(name)

    def list_tools(self) -> list[dict]:
        """
        Return all registered tools.
        """

        return [
            {
                "name": name,
                "description": tool["description"],
            }
            for name, tool in self.tools.items()
        ]