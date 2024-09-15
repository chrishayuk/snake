from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_agent import BaseTicTacToeAgent

class SmartTicTacToeAgent(BaseTicTacToeAgent):
    def __init__(self, id: str, name: str, description: str, player=1):
        # call parent initializer
        super().__init__(id, name, description, player)

    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC

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
