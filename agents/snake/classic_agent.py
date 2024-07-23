# File: agents/snake/classic_agent.py
import numpy as np
from typing import Tuple
from agents.agent_logging import AgentLogger
from agents.agent_type import AgentType
from agents.base_agent import BaseAgent
from agents.snake.agent_action import AgentAction


class ClassicAgent(BaseAgent):
    def __init__(self, id: str, name: str, description: str):
        # call the parent
        super().__init__(id, name, description)

        # set the default direction
        self.current_direction = AgentAction.RIGHT
    
    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC

    def get_snake_head_position(self, state: np.ndarray) -> Tuple[int, int]:
        """Extract the position of the snake's head from the state."""
        return tuple(np.argwhere(state[:,:,1] == 1)[0])

    def get_food_position(self, state: np.ndarray) -> Tuple[int, int]:
        """Extract the position of the food from the state."""
        return tuple(np.argwhere(state[:,:,2] == 1)[0])

    def get_snake_body_positions(self, state: np.ndarray) -> np.ndarray:
        """Extract the positions of the snake's body from the state."""
        return np.argwhere(state[:,:,1] == 1)
    
    def serialize_state(self, state: np.ndarray) -> list:
        """Convert numpy array state to a serializable list."""
        return state.tolist()

    def deserialize_state(self, state_list: list) -> np.ndarray:
        """Convert serialized list back to numpy array."""
        return np.array(state_list)
    
    def parse_state_string(self, state_str: str) -> np.ndarray:
        """Parse the state string representation into a numpy array."""
        grid_lines = state_str.split("\n")
        size = len(grid_lines[0].split())
        state = np.zeros((size, size, 4))

        for i, line in enumerate(grid_lines):
            elements = line.split()
            for j, element in enumerate(elements):
                if element == 'H':
                    state[i, j, 1] = 1
                elif element == 'O':
                    state[i, j, 0] = 1
                elif element == 'F':
                    state[i, j, 2] = 1
                elif element == '.':
                    state[i, j, 3] = 1  # Assuming empty spaces are represented in channel 3

        return state
    