import time
import numpy as np
from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_classic_agent import BaseTicTacToeClassicAgent

class SmartTicTacToeAgent(BaseTicTacToeClassicAgent):
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
        thought_process = f"Step {step}: Analyzing the current state:\n{state}\n"
        best_move = None

        # Describe marks on the board for both players
        player_1_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 1]
        player_2_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 2]

        thought_process += f"Player 1 has marks at {player_1_positions}.\n"
        thought_process += f"Player 2 has marks at {player_2_positions}.\n"

        # First, try to win the game with a move
        winning_move = self.find_winning_move(state, self.player)

        if winning_move:
            # Get the row and column from the winning move
            row, col = self.reverse_action_map[winning_move]
            
            # Temporarily apply the move to the board
            temp_state = np.copy(state)
            temp_state[row, col] = self.player
            
            # Check if it completes a row, column, or diagonal
            if np.all(temp_state[row, :] == self.player):
                thought_process += f"Found winning move at position {winning_move}, completing row {row}.\n"
            elif np.all(temp_state[:, col] == self.player):
                thought_process += f"Found winning move at position {winning_move}, completing column {col}.\n"
            elif row == col and np.all(np.diag(temp_state) == self.player):
                thought_process += f"Found winning move at position {winning_move}, completing diagonal.\n"
            elif row + col == 2 and np.all(np.diag(np.fliplr(temp_state)) == self.player):
                thought_process += f"Found winning move at position {winning_move}, completing anti-diagonal.\n"
            
            # Set the best move to the winning move
            best_move = winning_move

        else:
            thought_process += "No winning move found.\n"
            # If no winning move, check if we need to block the opponent
            opponent = 2 if self.player == 1 else 1
            thought_process += f"Checking for blocking move against opponent {opponent}...\n"

            blocking_move = self.find_winning_move(state, opponent)

            if blocking_move:
                # Explain why the move is a blocking move
                row, col = self.reverse_action_map[blocking_move]
                if np.all(state[row, :] == opponent):
                    thought_process += f"Opponent is trying to complete row {row}, blocking with move {blocking_move}.\n"
                elif np.all(state[:, col] == opponent):
                    thought_process += f"Opponent is trying to complete column {col}, blocking with move {blocking_move}.\n"
                elif row == col and np.all(np.diag(state) == opponent):
                    thought_process += f"Opponent is trying to complete diagonal, blocking with move {blocking_move}.\n"
                elif row + col == 2 and np.all(np.diag(np.fliplr(state)) == opponent):
                    thought_process += f"Opponent is trying to complete anti-diagonal, blocking with move {blocking_move}.\n"
                best_move = blocking_move
            else:
                thought_process += "No blocking move found.\n"
                # If no win or block, choose a random valid move
                best_move = self.get_random_move(state)
                thought_process += f"No immediate threats or winning moves found. Randomly selected move at position {best_move}.\n"

        # Log the final selected move and entire thought process
        thought_process += f"Final move selected: {best_move}.\n"

        # Log the decision with the logger
        time_of_action = time.strftime('%Y-%m-%d %H:%M:%S')

        # log the decision
        self.logger.log_decision(
            game_id=self.game_id,                 # The agent's ID (or game ID if applicable)
            step=step,                            # Current step in the game
            state=state,                          # Current board state
            thought_process=thought_process,      # Detailed thought process
            final_output=best_move,               # The chosen move
            response=best_move,                   # The chosen move
            time_completed=time_of_action,        # Timestamp of when the action was completed
            player='X' if self.player == 1 else 'O'         # log the player role
        )

        # Return the best move
        return best_move
