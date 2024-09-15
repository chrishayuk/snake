# File: agents/base_agent.py
from abc import ABC, abstractmethod
import time
from agents.agent_logging import AgentLogger

class BaseAgent(ABC):
    def __init__(self, id: str, name: str, description: str):
        # set the agent details
        self.id = id
        self.name = name
        self.description = description

        # Initialize logger with default values
        self.logger = AgentLogger(agent_id=self.id)

        # initalize reward
        self.reward = 0

    def add_reward(self, reward):
        """Increase the agent's total reward by the given amount."""
        self.reward += reward

    def reset_reward(self):
        """Reset the agent's reward at the start of a new game."""
        self.reward = 0

    @property
    def agent_type(self) -> str:
        """Return the type of the agent."""
        pass

    def game_over(self, step:int, state: str):
        # set the time completed
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')

        # log the state, thought process, and decision
        self.logger.log_decision(self.game_id, step, state, "", "", "", time_completed)