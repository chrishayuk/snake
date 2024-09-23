import numpy as np
import time
from agents.base_agent import BaseAgent
from agents.tic_tac_toe.base_tic_tac_toe_agent import BaseTicTacToeAgent

class BaseTicTacToeClassicAgent(BaseAgent, BaseTicTacToeAgent):
    def __init__(self, id: str, name: str, description: str, player=1):
        # call the parent
        super().__init__(id, name, description)

        # set the player
        self.player = player

    @property
    def agent_type(self) -> str:
        # not implemented
        raise NotImplementedError("This should be implemented by child classes.")

    def generate_thought_process(self, step: int, state, rendered_state: str, rationale: str, current_player: int) -> str:
        """
        Generates a standardized thought process log for decision-making.
        """
        thought_process = (
            f"Step {step}:\n"
            f"Analyzing the current state for player {current_player}:\n"
            f"{state}\n"
            f"Rendered state:\n{rendered_state}\n"
            f"Rationale:\n{rationale}\n"
        )
        return thought_process
    
    def log_decision_with_thoughts(self, step: int, state, rendered_state: str, current_player: int, best_move: int, rationale: str):
        """
        Logs the decision along with the generated thought process.
        """
        thought_process = self.generate_thought_process(step, state, rendered_state, rationale, current_player)
        time_of_action = time.strftime('%Y-%m-%d %H:%M:%S')
        
        self.logger.log_decision(
            game_id=self.game_id,
            step=step,
            state=state,
            rendered_state=rendered_state,
            thought_process=thought_process,
            final_output=best_move,
            response=best_move,
            time_completed=time_of_action,
            player='X' if current_player == 1 else 'O'
        )

    def get_action(self, step: int, state, rendered_state: str, current_player: int) -> int:
        """
        A template for all agents. Each agent will have its own logic for selecting the best move,
        but will always have this fallback mechanism.
        """
        rationale = "Evaluating potential moves based on current board state.\n"
        best_move = None

        # Each agent should have its own logic here (winning/blocking/etc.)

        # Fallback if no best_move is found
        if best_move is None:
            rationale += "No winning or blocking move found. Using fallback to select a random move.\n"
            best_move = self.get_random_move(state)

        # Log the decision and rationale
        self.log_decision_with_thoughts(step, state, rendered_state, current_player, best_move, rationale)

        return best_move
