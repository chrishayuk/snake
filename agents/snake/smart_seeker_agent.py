# File: smart_seeker_agent.py
import numpy as np
from typing import Tuple
from agents.base_agent import BaseAgent
from agents.snake.agent_action import AgentAction


class SmartSeekerAgent(BaseAgent):
    def __init__(self):
        self.current_direction = AgentAction.RIGHT  # Default initial direction

    @property
    def name(self) -> str:
        """Return the name of the agent."""
        return "Smart Seeker Agent"

    @property
    def agent_type(self) -> str:
        """Return the type of the agent."""
        return "Snake Agent"

    def get_snake_head_position(self, state: np.ndarray) -> Tuple[int, int]:
        """Extract the position of the snake's head from the state."""
        return tuple(np.argwhere(state[:,:,1] == 1)[0])

    def get_food_position(self, state: np.ndarray) -> Tuple[int, int]:
        """Extract the position of the food from the state."""
        return tuple(np.argwhere(state[:,:,2] == 1)[0])

    def get_snake_body_positions(self, state: np.ndarray) -> np.ndarray:
        """Extract the positions of the snake's body from the state."""
        return np.argwhere(state[:,:,1] == 1)

    def get_action(self, state: np.ndarray) -> AgentAction:
        # get the position of the snake head
        snake_head = self.get_snake_head_position(state)

        # get the food position
        food = self.get_food_position(state)

        # get the snake body positions
        snake_body = self.get_snake_body_positions(state)

        # Define the possible moves
        possible_moves = {
            AgentAction.UP: (snake_head[0] - 1, snake_head[1]),
            AgentAction.DOWN: (snake_head[0] + 1, snake_head[1]),
            AgentAction.LEFT: (snake_head[0], snake_head[1] - 1),
            AgentAction.RIGHT: (snake_head[0], snake_head[1] + 1),
        }

        # Define the opposite directions
        opposite_directions = {
            AgentAction.UP: AgentAction.DOWN,
            AgentAction.DOWN: AgentAction.UP,
            AgentAction.LEFT: AgentAction.RIGHT,
            AgentAction.RIGHT: AgentAction.LEFT,
        }

        # Filter out moves that would result in a collision with the snake's body or are opposite to current direction
        safe_moves = {
            action: pos for action, pos in possible_moves.items()
            if pos not in snake_body.tolist() and action != opposite_directions[self.current_direction]
        }

        # Determine the best move that gets closer to the food
        best_move = None
        min_distance = float('inf')
        
        for action, pos in safe_moves.items():
            distance = abs(food[0] - pos[0]) + abs(food[1] - pos[1])
            if distance < min_distance:
                min_distance = distance
                best_move = action

        # If no safe move is found, default to the first safe move
        if best_move is None:
            best_move = next(iter(safe_moves.keys()), AgentAction.UP)

        # Update the current direction
        self.current_direction = best_move

        return best_move
    