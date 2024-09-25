# File: agents/agent_type.py
from enum import Enum

class AgentType:
    CLASSIC = "Classic"
    LLM = "LLM Agent"
    HUMAN = "Human"


    @property
    def description(self) -> str:
        if self == AgentType.LLM:
            return "Agent that uses large language models for decision-making based on textual game state representations."
        elif self == AgentType.CLASSIC:
            return "Agent that uses traditional algorithmic or rule-based approaches for decision-making based on numerical game state representations."
        elif self == AgentType.HUMAN:
            return "Human Agent"
