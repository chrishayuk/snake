# File: agents/agent_action.py
from abc import ABC, abstractmethod

class AgentAction(ABC):

    @abstractmethod
    def __str__(self):
        pass

    @classmethod
    @abstractmethod
    def from_string(cls, action_str):
        pass
