import time
from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_agent import BaseTicTacToeAgent

class MiniMaxTicTacToeAgent(BaseTicTacToeAgent):

    def __init__(self, id: str, name: str, description: str, player=1):
        super().__init__(id, name, description, player)

    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC
    
    def get_action(self, step: int, state) -> int:
        """ 
        Use the Minimax algorithm to decide on the best action and log the decision.
        """
        best_score = -float('inf')
        best_move = None

        # Loop through available actions
        for action in self.get_available_actions(state):
            # Apply the action
            new_state = self.apply_action(state, action, self.player)

            # Start minimizing for the opponent
            score = self._minimax(new_state, 0, False) 

            # Check if this is the best score and action
            if score > best_score:
                best_score = score
                best_move = action

        # Log the decision with the logger
        time_of_action = time.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.log_decision(
            game_id=self.game_id,          # The agent's ID (or game ID if applicable)
            step=step,                     # Current step in the game
            state=state,                   # Current board state
            thought_process=f"best score was {best_score} for the best move {best_move}",  # Description of the decision-making process
            final_output=best_move,        # The best move chosen by the Minimax algorithm
            response=best_move,            # The best move chosen by the Minimax algorithm
            time_completed=time_of_action  # Timestamp of when the action was completed
        )

        # Return the best move
        return best_move

    
    def _minimax(self, state, depth, is_maximizing_player) -> int:
        """ The Minimax algorithm to calculate the best move. """
        winner = self.get_winner(state)

        # check if the winner is current player
        if winner == self.player:
            # Maximize the score for the agent, we'll work to a depth of 10 moves
            return 10 - depth  
        elif winner != 0 and winner is not None:
            # Minimize the score for the opponent
            return depth - 10  
        elif self.is_terminal(state):
            # Draw
            return 0  
        
        # check if we're the maximizing player
        if is_maximizing_player:
            # get the best score
            best_score = -float('inf')

            # loop through the available actions
            for action in self.get_available_actions(state):
                # get the the new state from applying action
                new_state = self.apply_action(state, action, self.player)
                
                # get best score from next node down
                score = self._minimax(new_state, depth + 1, False)

                # get best score
                best_score = max(score, best_score)

            # return the best score
            return best_score
        else:
            # get best score
            best_score = float('inf')

            # get the oopponent
            opponent = 1 if self.player == 2 else 2

            # loop through available actions
            for action in self.get_available_actions(state):
                new_state = self.apply_action(state, action, opponent)

                # get best score from next node down
                score = self._minimax(new_state, depth + 1, True)

                # get lowest score for the opponent
                best_score = min(score, best_score)

            # return the best (loewst) opponent score
            return best_score
