from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_agent import BaseTicTacToeAgent

class RandomTicTacToeAgent(BaseTicTacToeAgent):
    def __init__(self, id: str, name: str, description: str, player=1):
        # Call the parent constructor
        super().__init__(id, name, description, player)

    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC

    def get_action(self, step: int, state) -> int:
        """ Get a random valid action for the agent. """
        return self.get_random_move(state)
