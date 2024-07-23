# File: agents/base_agent.py
from abc import ABC, abstractmethod
from agents.agent_logging import AgentLogger

class BaseAgent(ABC):
    def __init__(self, id: str, name: str, description: str):
        # set the agent details
        self.id = id
        self.name = name
        self.description = description

        # Initialize logger with default values
        self.logger = AgentLogger(agent_id=self.id)

    @property
    def agent_type(self) -> str:
        """Return the type of the agent."""
        pass