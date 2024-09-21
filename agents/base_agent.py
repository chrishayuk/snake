# File: agents/base_agent.py
import time
import uuid
from abc import ABC, abstractmethod
from agents.agent_logging import AgentLogger

class BaseAgent(ABC):
    def __init__(self, id: str, name: str, description: str):
        # set the agent details
        self.unique_agent_id = str(uuid.uuid4())
        self.id = id
        self.name = name
        self.description = description

        # Initialize logger with default values
        self.logger = AgentLogger(agent_id=self.id, unique_agent_id=self.unique_agent_id)

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

    def game_over(self, step: int, state: str, rendered_state: str):
        # Set the time completed
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')

        # Log the final "Game Over" state
        self.logger.log_decision(
            game_id=self.game_id,
            step=step,
            state=state,  # This should be the final state (2D NumPy array or string)
            rendered_state=rendered_state,  # This is the rendered (visual) state of the board
            thought_process="Game Over",
            final_output="Game Over",
            response="Game Over",
            time_completed=time_completed,
            player=''  # No specific player for the Game Over state
        )
