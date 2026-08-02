from app.mcp.tools.story_tools import StoryTools

def register_story_tools(registry):
    """
    Register all story-related tools.
    """

    story_tools = StoryTools()

    registry.register(
        name="search_user_stories",
        description=(
            "Searches the user story knowledge base "
            "and returns relevant tickets."
        ),
        function=story_tools.search_user_stories,
    )