from app.models.user_story import UserStory

mock_stories = [
    UserStory(
        title="Update HCO_ID references",
        story_url="https://jira.example.com/AI-101",
        description=(
            "Update every database table that references HCO_ID "
            "to support the new identifier format."
        ),
        acceptance_criteria=(
            "- All referencing tables updated\n"
            "- Unit tests pass\n"
            "- No foreign key violations"
        ),
        feature="Member Management",
        priority="High",
        status="Ready for Development",
    ),
    UserStory(
        title="Refactor PDF generation service",
        story_url="https://jira.example.com/AI-102",
        description=(
            "Refactor the PDF generation module to improve "
            "maintainability and reduce duplication."
        ),
        acceptance_criteria=(
            "- Existing PDFs remain unchanged\n"
            "- Code coverage above 90%\n"
            "- Performance is not degraded"
        ),
        feature="Document Services",
        priority="Medium",
        status="Ready for Development",
    ),
    UserStory(
        title="Implement audit logging for user updates",
        story_url="https://jira.example.com/AI-103",
        description=(
            "Capture all user profile updates in the audit log."
        ),
        acceptance_criteria=(
            "- Every update is logged\n"
            "- Timestamp and user recorded\n"
            "- Logs are searchable"
        ),
        feature="Security",
        priority="High",
        status="In Progress",
    ),
]