from dataclasses import dataclass

@dataclass
class Response:
    story_title: str
    story_url: str
    feature: str
    priority: str
    acceptance_criteria: str
    notes: str
    testing_scenarios: str