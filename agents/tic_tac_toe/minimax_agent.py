import time
import random
import numpy as np
from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_classic_agent import BaseTicTacToeClassicAgent


class MiniMaxTicTacToeAgent(BaseTicTacToeClassicAgent):

    def __init__(self, id: str, name: str, description: str, player=1):
        super().__init__(id, name, description, player)

    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC
    
    def get_action(self, step: int, state, rendered_state: str, current_player: int) -> int:
        # set the rationale
        rationale = "Using Minimax algorithm to evaluate possible moves.\n"

        # initialize
        best_move = None
        best_score = -float('inf')

        # Loop through available actions and find the best one using Minimax
        for action in self.get_available_actions(state):
            # get the new state and score
            new_state = self.apply_action(state, action, self.player)
            score = self._minimax(new_state, 0, False)

            # add the evaluation and score
            rationale += f"Evaluating action {action}, score: {score}.\n"

            # check if this the best score
            if score > best_score:
                best_score = score
                best_move = action

        # set the rationale
        rationale += f"Best move determined by Minimax is at position {best_move} with score {best_score}.\n"

        # If no best move is found, fallback to a random move from available options
        if best_move is None:
            rationale += "No best move found. Using fallback to select a random move.\n"
            best_move = self.get_random_move(state)
        
        # Log decision
        self.log_decision_with_thoughts(step, state, rendered_state, current_player, best_move, rationale)

        # return the best move
        return best_move

    def _minimax(self, state, depth, is_maximizing_player) -> int:
        """ The Minimax algorithm to calculate the best move. """
        winner = self.get_winner(state)

        # Terminal conditions: return scores for win, loss, or draw
        if winner == self.player:
            return 10 - depth  # Maximize the score for the agent, prioritize quicker wins
        elif winner == (3 - self.player):
            return depth - 10  # Minimize the score for the opponent, penalize quicker losses
        elif self.is_terminal(state):
            return 0  # Draw

        if is_maximizing_player:
            best_score = -float('inf')
            for action in self.get_available_actions(state):
                new_state = self.apply_action(state, action, self.player)
                score = self._minimax(new_state, depth + 1, False)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            opponent = 3 - self.player
            for action in self.get_available_actions(state):
                new_state = self.apply_action(state, action, opponent)
                score = self._minimax(new_state, depth + 1, True)
                best_score = min(score, best_score)
            return best_score


    def is_terminal(self, state) -> bool:
        """Check if the game is in a terminal state (win or draw)."""
        return self.get_winner(state) is not None or not np.any(state == 0)

    def get_winner(self, state):
        """Return the winner if there's one. Returns 1 for 'X', 2 for 'O', and None for no winner."""
        for player in [1, 2]:
            # Check rows, columns, and diagonals for a win
            if any(np.all(state[row, :] == player) for row in range(3)) or \
               any(np.all(state[:, col] == player) for col in range(3)) or \
               np.all(np.diag(state) == player) or \
               np.all(np.diag(np.fliplr(state)) == player):
                return player
        return None if np.any(state == 0) else 0  # 0 indicates a draw
