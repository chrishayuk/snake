# File: simple_agent.py
import numpy as np
from typing import Tuple
from agents.agent_action import AgentAction

class SimpleAgent:
    def __init__(self):
        pass

    def get_snake_head_position(self, state: np.ndarray) -> Tuple[int, int]:
        """Extract the position of the snake's head from the state."""
        return tuple(np.argwhere(state[:,:,1] == 1)[0])

    def get_food_position(self, state: np.ndarray) -> Tuple[int, int]:
        """Extract the position of the food from the state."""
        return tuple(np.argwhere(state[:,:,2] == 1)[0])

    def get_action(self, state: np.ndarray) -> AgentAction:
        # get the position of the snake head
        snake_head = self.get_snake_head_position(state)

        # get the food position
        food = self.get_food_position(state)
        
        # Head towards the food policy
        if food[0] < snake_head[0]:
            return AgentAction.UP
        elif food[0] > snake_head[0]:
            return AgentAction.DOWN
        elif food[1] < snake_head[1]:
            return AgentAction.LEFT
        else:
            return AgentAction.RIGHT