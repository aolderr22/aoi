from dataclasses import dataclass

@dataclass
class UserStory:
    title: str
    story_url: str
    description: str
    acceptance_criteria: str
    feature: str
    priority: str
    status: str