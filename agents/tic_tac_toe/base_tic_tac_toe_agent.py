import random
import numpy as np

class BaseTicTacToeAgent:
    # action map
    action_map = {
        (0, 0): 1, (0, 1): 2, (0, 2): 3,
        (1, 0): 4, (1, 1): 5, (1, 2): 6,
        (2, 0): 7, (2, 1): 8, (2, 2): 9
    }
    
    # reverse action map
    reverse_action_map = {v: k for k, v in action_map.items()}  # Reverse map for action to (row, col)

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
            return True
        return False
    
    def get_winner(self, state):
        """ Return the winner if there's one. Returns 1 for 'X', 2 for 'O', and None for no winner. """
        for player in [1, 2]:
            if self.find_winning_move(state, player):
                return player
        return None if np.any(state == 0) else 0  # 0 indicates a draw
    
    def find_winning_move(self, state, player):
        """
        Check if there is a winning move available for the given player.
        If so, return the action (position 1-9) that will complete the win.
        Otherwise, return None.
        """
        # Check rows
        for row in range(3):
            if np.sum(state[row, :] == player) == 2 and np.sum(state[row, :] == 0) == 1:
                col = np.where(state[row, :] == 0)[0][0]
                return self.action_map[(row, col)]

        # Check columns
        for col in range(3):
            if np.sum(state[:, col] == player) == 2 and np.sum(state[:, col] == 0) == 1:
                row = np.where(state[:, col] == 0)[0][0]
                return self.action_map[(row, col)]

        # Check diagonal (top-left to bottom-right)
        if np.sum(np.diag(state) == player) == 2 and np.sum(np.diag(state) == 0) == 1:
            diag_index = np.where(np.diag(state) == 0)[0][0]
            return self.action_map[(diag_index, diag_index)]

        # Check anti-diagonal (top-right to bottom-left)
        if np.sum(np.diag(np.fliplr(state)) == player) == 2 and np.sum(np.diag(np.fliplr(state)) == 0) == 1:
            anti_diag_index = np.where(np.diag(np.fliplr(state)) == 0)[0][0]
            return self.action_map[(anti_diag_index, 2 - anti_diag_index)]

        # No winning move found
        return None

    def get_available_actions(self, state) -> list:
        """ Return the list of available actions (1-9) based on the current board state. """
        empty_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 0]
        return [self.action_map[(r, c)] for (r, c) in empty_positions]
    
    def apply_action(self, state, action, player):
        """ Apply an action to the board and return the resulting state. """
        row, col = self.reverse_action_map[action]
        new_state = np.copy(state)
        new_state[row, col] = player
        return new_state
