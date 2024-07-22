# File: adaptive_hamiltonian_agent.py
import numpy as np
from typing import Tuple
from agents.base_agent import BaseAgent
from agents.snake.agent_action import AgentAction

class AdaptiveHamiltonianAgent(BaseAgent):
    def __init__(self, grid_size: Tuple[int, int]):
        self.grid_size = grid_size
        self.steps_since_last_food = 0
        self.current_direction = AgentAction.RIGHT  # Default initial direction

    @property
    def name(self) -> str:
        """Return the name of the agent."""
        return "Adaptive Hamiltonian Agent"

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

    def get_possible_moves(self, snake_head: Tuple[int, int]) -> dict:
        """Define possible moves from the current position."""
        return {
            AgentAction.UP: (snake_head[0] - 1, snake_head[1]),
            AgentAction.DOWN: (snake_head[0] + 1, snake_head[1]),
            AgentAction.LEFT: (snake_head[0], snake_head[1] - 1),
            AgentAction.RIGHT: (snake_head[0], snake_head[1] + 1),
        }

    def get_safe_moves(self, possible_moves: dict, snake_body: np.ndarray, avoid_direction: AgentAction) -> dict:
        """Filter out moves that would result in a collision with the snake's body or are opposite to current direction."""
        snake_body_list = snake_body.tolist()
        return {
            action: pos for action, pos in possible_moves.items()
            if pos not in snake_body_list and action != avoid_direction
        }

    def get_action(self, state: np.ndarray) -> AgentAction:
        snake_head = self.get_snake_head_position(state)
        food = self.get_food_position(state)
        snake_body = self.get_snake_body_positions(state)

        # If the snake has gone 50 steps without food, move towards the food aggressively
        if self.steps_since_last_food >= 50:
            target_position = food
        else:
            target_position = food

        possible_moves = self.get_possible_moves(snake_head)
        opposite_directions = {
            AgentAction.UP: AgentAction.DOWN,
            AgentAction.DOWN: AgentAction.UP,
            AgentAction.LEFT: AgentAction.RIGHT,
            AgentAction.RIGHT: AgentAction.LEFT,
        }

        safe_moves = self.get_safe_moves(possible_moves, snake_body, opposite_directions[self.current_direction])

        best_move = None
        min_distance = float('inf')

        for action, pos in safe_moves.items():
            distance = abs(target_position[0] - pos[0]) + abs(target_position[1] - pos[1])
            if distance < min_distance:
                min_distance = distance
                best_move = action

        if not best_move:
            best_move = next(iter(safe_moves.keys()), AgentAction.UP)

        self.current_direction = best_move
        self.steps_since_last_food += 1

        if snake_head == food:
            self.steps_since_last_food = 0

        return best_move
