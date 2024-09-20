import time
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

    def get_action(self, step: int, state) -> int:
        """
        Get a random valid action for the agent and log the decision.
        """
        # Get a random move
        random_move = self.get_random_move(state)

        # Log the decision with the logger
        time_of_action = time.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.log_decision(
            game_id=self.game_id,                # The agent's ID (or game ID if applicable)
            step=step,                      # Current step in the game
            state=state,                    # Current board state
            thought_process="Random choice", # Description of the decision-making process
            final_output=random_move,       # The randomly selected move
            response=random_move,           # No specific response (optional for random agent)
            time_completed=time_of_action   # Timestamp of when the action was completed
        )

        # Return the random move
        return random_move
