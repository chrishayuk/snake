import random
from agents.base_agent import BaseAgent

class RandomTicTacToeAgent(BaseAgent):
    def __init__(self, id: str, name: str, description: str, player=1):
        # Call the parent constructor with id, name, and description
        super().__init__(id, name, description)
        self.player = player  # The agent's player (1 for 'X' or 2 for 'O')

    @property
    def agent_type(self) -> str:
        """Return the type of the agent."""
        return "Random Tic-Tac-Toe"

    def get_action(self, step: int, state) -> int:
        """
        Get a random valid action for the agent.
        - state: The current game board as a 3x3 array.
        - Returns an action (number between 1 and 9) representing the agent's chosen move.
        """
        return self.get_random_move(state)

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
