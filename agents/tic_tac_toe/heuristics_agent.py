from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_agent import BaseTicTacToeAgent

class HeuristicsTicTacToeAgent(BaseTicTacToeAgent):
    
    def __init__(self, id: str, name: str, description: str, player=1):
        super().__init__(id, name, description, player)
    
    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC
    
    def get_action(self, step: int, state) -> int:
        """
        Decide on an action using a series of heuristics.
        """
        # 1. Winning move
        for action in self.get_available_actions(state):
            new_state = self.apply_action(state, action, self.player)
            if self.find_winning_move(new_state, self.player):
                return action

        # 2. Blocking opponent's winning move
        opponent = 1 if self.player == 2 else 2
        for action in self.get_available_actions(state):
            new_state = self.apply_action(state, action, opponent)
            if self.find_winning_move(new_state, opponent):
                return action

        # 3. Take the center
        if 5 in self.get_available_actions(state):
            return 5

        # 4. Take a corner (1, 3, 7, 9)
        for corner in [1, 3, 7, 9]:
            if corner in self.get_available_actions(state):
                return corner

        # 5. Take any other random move
        return self.get_random_move(state)
