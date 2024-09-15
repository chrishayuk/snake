import random
import numpy as np
from agents.base_agent import BaseAgent

class BaseTicTacToeAgent(BaseAgent):
    # action map
    action_map = {
        (0, 0): 1, (0, 1): 2, (0, 2): 3,
        (1, 0): 4, (1, 1): 5, (1, 2): 6,
        (2, 0): 7, (2, 1): 8, (2, 2): 9
    }
    
    # reverse action map
    reverse_action_map = {v: k for k, v in action_map.items()}  # Reverse map for action to (row, col)

    def __init__(self, id: str, name: str, description: str, player=1):
        super().__init__(id, name, description)
        self.player = player  # The agent's player (1 for 'X' or 2 for 'O')

    @property
    def agent_type(self) -> str:
        """Return the type of the agent (to be implemented by child classes)."""
        raise NotImplementedError("This should be implemented by child classes.")

    def find_winning_move(self, state, player):
        """ Check if placing a mark results in a win for the given player. """
        # Check rows, columns, and diagonals for a win
        return (
            any(np.all(state[row, :] == player) for row in range(3)) or
            any(np.all(state[:, col] == player) for col in range(3)) or
            np.all(np.diag(state) == player) or
            np.all(np.diag(np.fliplr(state)) == player)
        )

    def get_random_move(self, state) -> int:
        """ Return a random valid move (number between 1 and 9) from the current state. """
        # get empty positions
        empty_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 0]

        # check if we have empty positions
        if empty_positions:
            # make a random choice
            row, col = random.choice(empty_positions)

            # return the action
            return self.action_map[(row, col)]
        return None
    
    def is_terminal(self, state) -> bool:
        """ Check if the game is in a terminal state (win or draw). """
        if self.get_winner(state) is not None or not np.any(state == 0):
            # we got a winner or a draw
            return True
        
        # not a terminal state
        return False
    
    def get_winner(self, state):
        """ Return the winner if there's one. Returns 1 for 'X', 2 for 'O', and None for no winner. """
        # for each player
        for player in [1, 2]:
            # check if the current play is a winning move
            if self.find_winning_move(state, player):
                # return the winning player
                return player
        
        # was a draw
        return None if np.any(state == 0) else 0  # 0 indicates a draw
    
    def get_available_actions(self, state) -> list:
        """ Return the list of available actions (1-9) based on the current board state. """
        # get empty positions
        empty_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 0]

        # return the actions from the action map for the empty positions
        return [self.action_map[(r, c)] for (r, c) in empty_positions]
    
    def apply_action(self, state, action, player):
        """ Apply an action to the board and return the resulting state. """
        # get row and column for the action, from the action map
        row, col = self.reverse_action_map[action]

        # get a copy of the current state
        new_state = np.copy(state)

        # apply the (x or o) to the board position
        new_state[row, col] = player

        # return the new state
        return new_state
