import time
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
        Decide on an action using a series of heuristics, and log the decision.
        """
        best_move = None
        description = ""
        
        # 1. Winning move
        for action in self.get_available_actions(state):
            new_state = self.apply_action(state, action, self.player)
            if self.find_winning_move(new_state, self.player):
                best_move = action
                description = "Winning move"
                break
        
        # 2. Blocking opponent's winning move
        if not best_move:
            opponent = 1 if self.player == 2 else 2
            for action in self.get_available_actions(state):
                new_state = self.apply_action(state, action, opponent)
                if self.find_winning_move(new_state, opponent):
                    best_move = action
                    description = "Blocking opponent's winning move"
                    break

        # 3. Take the center
        if not best_move and 5 in self.get_available_actions(state):
            best_move = 5
            description = "Taking the center"

        # 4. Take a corner (1, 3, 7, 9)
        if not best_move:
            for corner in [1, 3, 7, 9]:
                if corner in self.get_available_actions(state):
                    best_move = corner
                    description = "Taking a corner"
                    break

        # 5. Take any other random move
        if not best_move:
            best_move = self.get_random_move(state)
            description = "Taking a random move"

        # Log the decision with the logger
        time_of_action = time.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.log_decision(self.game_id, step, state, description, best_move, None, time_of_action)

        return best_move
