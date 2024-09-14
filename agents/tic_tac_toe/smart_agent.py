import random
import numpy as np
from agents.base_agent import BaseAgent

class SmartTicTacToeAgent(BaseAgent):
    def __init__(self, id: str, name: str, description: str, player=1):
        # Call the parent constructor with id, name, and description
        super().__init__(id, name, description)
        self.player = player  # The agent's player (1 for 'X' or 2 for 'O')

    @property
    def agent_type(self) -> str:
        """Return the type of the agent."""
        return "Smart Tic-Tac-Toe"

    def get_action(self, step: int, state) -> int:
        """
        Get the best action for the agent.
        - state: The current game board as a 3x3 array.
        - Returns an action (number between 1 and 9) representing the agent's chosen move.
        """
        # First, try to win the game with a move
        move = self.check_for_win(state, self.player)
        if move:
            return move

        # If no winning move, check if we need to block the opponent
        opponent = 2 if self.player == 1 else 1
        move = self.check_for_win(state, opponent)
        if move:
            return move

        # If no win or block, choose a random valid move
        return self.get_random_move(state)

    def check_for_win(self, state, player) -> int:
        """
        Check if there is a winning move for the given player.
        - player: The current player (1 or 2).
        - Returns an action (number between 1 and 9) if a win is found, otherwise None.
        """
        action_map = {
            (0, 0): 1, (0, 1): 2, (0, 2): 3,
            (1, 0): 4, (1, 1): 5, (1, 2): 6,
            (2, 0): 7, (2, 1): 8, (2, 2): 9
        }

        for row in range(3):
            for col in range(3):
                if state[row, col] == 0:  # Check if the cell is empty
                    # Simulate placing the player's mark
                    state[row, col] = player
                    if self.is_winning_move(state, player):
                        state[row, col] = 0  # Reset the simulated move
                        return action_map[(row, col)]  # Return the corresponding action (1-9)
                    state[row, col] = 0  # Reset the simulated move
        return None

    def is_winning_move(self, state, player):
        """
        Check if placing a mark results in a win for the given player.
        """
        # Check rows, columns, and diagonals for a win
        return (
            any(np.all(state[row, :] == player) for row in range(3)) or
            any(np.all(state[:, col] == player) for col in range(3)) or
            np.all(np.diag(state) == player) or
            np.all(np.diag(np.fliplr(state)) == player)
        )

    def get_random_move(self, state) -> int:
        """
        Return a random valid move (number between 1 and 9) from the current state.
        """
        action_map = {
            (0, 0): 1, (0, 1): 2, (0, 2): 3,
            (1, 0): 4, (1, 1): 5, (1, 2): 6,
            (2, 0): 7, (2, 1): 8, (2, 2): 9
        }

        empty_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 0]
        if empty_positions:
            row, col = random.choice(empty_positions)
            return action_map[(row, col)]
        return None
