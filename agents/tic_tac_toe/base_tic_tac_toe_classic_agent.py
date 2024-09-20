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
