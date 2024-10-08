import time
from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_classic_agent import BaseTicTacToeClassicAgent

class HeuristicsTicTacToeAgent(BaseTicTacToeClassicAgent):
    
    def __init__(self, id: str, name: str, description: str, player=1):
        super().__init__(id, name, description, player)
    
    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC

    def check_two_way_win(self, state):
        """
        Check if a move sets up a two-way win for the player (i.e., a situation where 
        two winning moves are possible in the next turn).
        
        Returns the move that sets up the two-way win if found, otherwise None.
        """
        for action in self.get_available_actions(state):
            new_state = self.apply_action(state, action, self.player)
            win_count = 0
            for next_action in self.get_available_actions(new_state):
                next_state = self.apply_action(new_state, next_action, self.player)
                if self.find_winning_move(next_state, self.player):
                    win_count += 1
                if win_count >= 2:
                    return action  # Return the move that creates two winning options
        return None  # No two-way win found

    
    def get_action(self, step: int, state, rendered_state: str, current_player: int) -> int:
        # set the rationale
        rationale = "Checking for a winning move, blocking opponent, and strategic placements.\n"

        # initialize
        best_move = None

        # 1. Winning move
        for action in self.get_available_actions(state):
            new_state = self.apply_action(state, action, self.player)
            if self.find_winning_move(new_state, self.player):
                best_move = action
                rationale += f"Found a winning move at position {best_move}.\n"
                break

        # 2. Block opponent’s winning move
        if not best_move:
            opponent = 1 if self.player == 2 else 2
            for action in self.get_available_actions(state):
                new_state = self.apply_action(state, action, opponent)
                if self.find_winning_move(new_state, opponent):
                    best_move = action
                    rationale += f"Blocking opponent's winning move at position {best_move}.\n"
                    break

        # 3. Set up a two-way win
        if not best_move:
            rationale += "Checking if a two-way win can be set up...\n"
            two_way_win_move = self.check_two_way_win(state)
            if two_way_win_move:
                best_move = two_way_win_move
                rationale += f"Setting up a two-way win with move at position {best_move}.\n"

        # If no best move is found, fallback to a random move from available options
        if best_move is None:
            rationale += "No immediate winning or blocking move was found. Falling back to a random move based on available options.\n"
            best_move = self.get_random_move(state)

        # Log the decision with the final best move and rationale
        self.log_decision_with_thoughts(step, state, rendered_state, current_player, best_move, rationale)

        # Return the best move (or the fallback move if none found)
        return best_move
