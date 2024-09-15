import random
import numpy as np
from agents.base_agent import BaseAgent

class BaseTicTacToeAgent(BaseAgent):
    action_map = {
        (0, 0): 1, (0, 1): 2, (0, 2): 3,
        (1, 0): 4, (1, 1): 5, (1, 2): 6,
        (2, 0): 7, (2, 1): 8, (2, 2): 9
    }

    def __init__(self, id: str, name: str, description: str, player=1):
        super().__init__(id, name, description)
        self.player = player  # The agent's player (1 for 'X' or 2 for 'O')

    @property
    def agent_type(self) -> str:
        """Return the type of the agent (to be implemented by child classes)."""
        raise NotImplementedError("This should be implemented by child classes.")

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
        empty_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 0]
        if empty_positions:
            row, col = random.choice(empty_positions)
            return self.action_map[(row, col)]
        return None
    
    def is_terminal(self, state) -> bool:
        """
        Check if the game is in a terminal state (win or draw).
        """
        # If there's a winner or no empty spaces left (draw), it's terminal
        if self.get_winner(state) is not None or not np.any(state == 0):
            return True
        return False
    
    def get_winner(self, state):
        """
        Return the winner if there's one. Returns 1 for 'X', 2 for 'O', and None for no winner.
        """
        for player in [1, 2]:
            if self.is_winning_move(state, player):
                return player
        return None if np.any(state == 0) else 0  # 0 indicates a draw
    
    def get_available_actions(self, state) -> list:
        """
        Return the list of available actions (1-9) based on the current board state.
        """
        action_map = {
            (0, 0): 1, (0, 1): 2, (0, 2): 3,
            (1, 0): 4, (1, 1): 5, (1, 2): 6,
            (2, 0): 7, (2, 1): 8, (2, 2): 9
        }
        empty_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 0]
        return [action_map[(r, c)] for (r, c) in empty_positions]
    
    def apply_action(self, state, action, player):
        """
        Apply an action to the board and return the resulting state.
        """
        action_map = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 9: (2, 2)
        }
        row, col = action_map[action]
        new_state = np.copy(state)
        new_state[row, col] = player
        return new_state
