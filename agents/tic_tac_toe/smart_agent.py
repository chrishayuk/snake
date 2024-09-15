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
        Get the best action for the agent and log the decision.
        - state: The current game board as a 3x3 array.
        - Returns an action (number between 1 and 9) representing the agent's chosen move.
        """
        thought_process = ""
        best_move = None

        # First, try to win the game with a move
        move = self.find_winning_move(state, self.player)
        if move:
            best_move = move
            thought_process = "Trying to win the game"
        else:
            # If no winning move, check if we need to block the opponent
            opponent = 2 if self.player == 1 else 1
            move = self.find_winning_move(state, opponent)
            if move:
                best_move = move
                thought_process = "Blocking opponent's winning move"
            else:
                # If no win or block, choose a random valid move
                best_move = self.get_random_move(state)
                thought_process = "No winning/blocking move, choosing random move"

        # Log the decision with the logger
        time_of_action = time.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.log_decision(
            game_id=self.id,                 # The agent's ID (or game ID if applicable)
            step=step,                       # Current step in the game
            state=state,                     # Current board state
            thought_process=thought_process, # Description of the decision-making process
            final_output=best_move,          # The chosen move
            response=None,                   # No additional response needed
            time_completed=time_of_action    # Timestamp of when the action was completed
        )

        # Return the best move
        return best_move

