from app.models.user_story import UserStory

USER_STORIES = [
    UserStory(
        title="Update HCO_ID references",
        story_url="https://jira.example.com/ABC-101",
        description=(
            "Update database tables that reference HCO_ID "
            "to support the new identifier format."
        ),
        acceptance_criteria=(
            "1. Identify all tables containing HCO_ID.\n"
            "2. Create migration scripts.\n"
            "3. Validate data integrity after migration."
        ),
        feature="Healthcare Organization Management",
        priority="High",
        status="Ready for Development",
    ),

    UserStory(
        title="Refactor PDF generation service",
        story_url="https://jira.example.com/ABC-102",
        description=(
            "Refactor the PDF generation module to improve "
            "maintainability and reduce duplicated code."
        ),
        acceptance_criteria=(
            "1. Existing PDFs remain unchanged.\n"
            "2. Improve unit test coverage.\n"
            "3. Remove duplicated logic."
        ),
        feature="Document Services",
        priority="Medium",
        status="Ready for Development",
    ),

    UserStory(
        title="Add audit logging for user updates",
        story_url="https://jira.example.com/ABC-103",
        description=(
            "Capture changes made to user profiles "
            "for auditing purposes."
        ),
        acceptance_criteria=(
            "1. Store previous and new values.\n"
            "2. Record timestamp.\n"
            "3. Identify the user making changes."
        ),
        feature="Security",
        priority="High",
        status="Ready for Development",
    ),
]