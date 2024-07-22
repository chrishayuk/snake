# File: app/agents/base_agent.py
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the agent."""
        pass

    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Return the type of the agent."""
        pass