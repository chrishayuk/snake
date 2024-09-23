import time
import numpy as np
from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_classic_agent import BaseTicTacToeClassicAgent

class SmartTicTacToeAgent(BaseTicTacToeClassicAgent):
    def __init__(self, id: str, name: str, description: str, player=1):
        # call parent initializer
        super().__init__(id, name, description, player)

    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC

    def get_action(self, step: int, state, rendered_state: str, current_player: int) -> int:
        # Set the rationale for decision-making
        rationale = "Checking for winning or blocking moves.\n"

        # Initialize the best move to None
        best_move = None

        # Check for winning move
        winning_move = self.find_winning_move(state, current_player)

        if winning_move:
            # Set the rationale for a winning move
            rationale += f"Found winning move at position {winning_move}.\n"
            best_move = winning_move
        else:
            # Block opponent's winning move
            opponent = 1 if current_player == 2 else 2
            blocking_move = self.find_winning_move(state, opponent)

            if blocking_move:
                # Set the rationale for blocking the opponent
                rationale += f"Blocked opponent's winning move at position {blocking_move}.\n"
                best_move = blocking_move

        # If no best move is found, fallback to a random move from available options
        if best_move is None:
            rationale += "No winning or blocking move found. Using fallback to select a random move.\n"
            best_move = self.get_random_move(state)

        # Log the decision with the final best move and rationale
        self.log_decision_with_thoughts(step, state, rendered_state, current_player, best_move, rationale)

        # Return the best move (or the fallback move if none found)
        return best_move
