from agents.tic_tac_toe.base_tic_tac_toe_agent import BaseTicTacToeAgent

class SmartTicTacToeAgent(BaseTicTacToeAgent):
    def __init__(self, id: str, name: str, description: str, player=1):
        # call parent initializer
        super().__init__(id, name, description, player)

    @property
    def agent_type(self) -> str:
        """Return the type of the agent."""
        return "Smart Tic-Tac-Toe"
    
    def find_winning_move(self, state, player) -> int:
        """
        Find a winning move for the given player.
        - player: The current player (1 or 2).
        - Returns an action (number between 1 and 9) if a win is found, otherwise None.
        """
        for row in range(3):
            for col in range(3):
                if state[row, col] == 0:  # Check if the cell is empty
                    # Simulate placing the player's mark
                    state[row, col] = player
                    if self.is_winning_move(state, player):
                        state[row, col] = 0  # Reset the simulated move
                        return self.action_map[(row, col)]  # Return the corresponding action (1-9)
                    state[row, col] = 0  # Reset the simulated move
        return None

    def get_action(self, step: int, state) -> int:
        """
        Get the best action for the agent.
        - state: The current game board as a 3x3 array.
        - Returns an action (number between 1 and 9) representing the agent's chosen move.
        """
        # First, try to win the game with a move
        move = self.find_winning_move(state, self.player)
        if move:
            return move

        # If no winning move, check if we need to block the opponent
        opponent = 2 if self.player == 1 else 1
        move = self.find_winning_move(state, opponent)
        if move:
            return move

        # If no win or block, choose a random valid move
        return self.get_random_move(state)
