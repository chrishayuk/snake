# File: agents/base_agent.py
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, id: str, name: str, description: str):
        # set the agent details
        self.id = id
        self.name = name
        self.description = description

    @property
    def agent_type(self) -> str:
        """Return the type of the agent."""
        pass