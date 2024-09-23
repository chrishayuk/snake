import time
import numpy as np
from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_classic_agent import BaseTicTacToeClassicAgent

class RandomTicTacToeAgent(BaseTicTacToeClassicAgent):
    def __init__(self, id: str, name: str, description: str, player=1):
        # Call the parent constructor
        super().__init__(id, name, description, player)

    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC

    def get_action(self, step: int, state, rendered_state: str, current_player: int) -> int:
        # set the rationale
        rationale = "Choosing a random move as no specific strategy is applied for this agent.\n"

        # get the best move
        best_move = self.get_random_move(state)

        if best_move is not None:
            # set the rationale
            rationale += f"Randomly selected move at position {best_move}.\n"
        else:
            # set the rationale
            rationale += "No available moves to select randomly.\n"

        # Log decision
        self.log_decision_with_thoughts(step, state, rendered_state, current_player, best_move, rationale)

        # return the move
        return best_move

