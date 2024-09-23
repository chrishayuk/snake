import numpy as np
import time
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
        raise NotImplementedError("This should be implemented by child classes.")

    def check_potential_two_way_win(self, state, player: int) -> int:
        """
        Check if a move sets up a two-way win for the player, meaning that after making this move,
        the player will have two different ways to win on the next turn.
        
        Args:
        - state: The current game board as a 3x3 array.
        - player: The player to check for a two-way win scenario (1 or 2).

        Returns:
        - The action (1-9) that sets up a two-way win, or None if no such move exists.
        """
        available_actions = self.get_available_actions(state)
        for action in available_actions:
            # Apply the action for the player
            new_state = self.apply_action(state, action, player)
            
            # Check how many winning moves the player would have on the next turn
            win_count = 0
            for next_action in self.get_available_actions(new_state):
                next_state = self.apply_action(new_state, next_action, player)
                if self.find_winning_move(next_state, player):
                    win_count += 1
                
                # If the player has at least 2 winning moves, this is a two-way win
                if win_count >= 2:
                    return action  # This move sets up a two-way win
        
        return None  # No two-way win setup found


    def generate_thought_process(self, step: int, state, current_player: int, winning_move: int = None, blocking_move: int = None) -> str:
        """
        Generates a standardized thought process that analyzes the current board state retrospectively.
        This analysis is independent of the selected move.
        """
        # Analyze the current state of the board
        player_1_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 1]
        player_2_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 2]

        thought_process = (
            f"Step {step}:\n"
            f"Analyzing the current state of the board for player {current_player}:\n"
            f"{state}\n"
            f"Player 1 (X) positions: {player_1_positions}\n"
            f"Player 2 (O) positions: {player_2_positions}\n"
        )

        # Check for winning moves and blocking opportunities
        thought_process += "Checking for a potential winning move for both players...\n"
        winning_move_player_1 = self.find_winning_move(state, 1)
        winning_move_player_2 = self.find_winning_move(state, 2)

        if winning_move_player_1:
            thought_process += f"Player 1 (X) has a potential winning move at {winning_move_player_1}.\n"
        else:
            thought_process += "Player 1 (X) has no immediate winning move.\n"

        if winning_move_player_2:
            thought_process += f"Player 2 (O) has a potential winning move at {winning_move_player_2}.\n"
        else:
            thought_process += "Player 2 (O) has no immediate winning move.\n"

        # Check for blocking move
        if blocking_move:
            thought_process += f"Player {current_player} may need to block the opponent's winning move at position {blocking_move}.\n"

        # Check for potential two-way wins
        thought_process += "Checking for advanced strategies like setting up a two-way win...\n"
        two_way_win_setup = self.check_potential_two_way_win(state, current_player)
        if two_way_win_setup:
            thought_process += f"Player {current_player} can set up a two-way win by moving at {two_way_win_setup}.\n"
        else:
            thought_process += "No immediate opportunity for a two-way win setup found.\n"

        return thought_process


    def log_decision_with_thoughts(self, step: int, state, rendered_state: str, current_player: int, best_move: int, rationale: str, winning_move: int = None, blocking_move: int = None):
        """
        Logs the decision along with the generated thought process and rationale.
        """
        # Generate the board analysis (thought process)
        thought_process = self.generate_thought_process(step, state, current_player, winning_move, blocking_move)

        # Combine rationale for the selected move
        final_thoughts = thought_process + f"Rationale for selecting move {best_move}:\n{rationale}\n"

        # If this is a game-winning move, log that explicitly
        if winning_move:
            final_thoughts += f"Move {best_move} resulted in a win by completing row/column/diagonal.\n"

        # Log the decision with the combined thought process and rationale
        time_of_action = time.strftime('%Y-%m-%d %H:%M:%S')

        self.logger.log_decision(
            game_id=self.game_id,
            step=step,
            state=state,
            rendered_state=rendered_state,
            thought_process=final_thoughts,
            final_output=best_move,
            response=best_move,
            time_completed=time_of_action,
            player='X' if current_player == 1 else 'O'
        )


    def get_action(self, step: int, state, rendered_state: str, current_player: int) -> int:
        """
        A template for all agents. Each agent will have its own logic for selecting the best move,
        but will always have this fallback mechanism.
        """
        rationale = "Evaluating potential moves based on current board state.\n"
        best_move = None
        winning_move = None
        blocking_move = None

        # Check for a winning move
        winning_move = self.find_winning_move(state, current_player)
        if winning_move:
            best_move = winning_move
            rationale += f"Found a winning move at position {winning_move}.\n"

        # Check for blocking opponent's winning move
        if not best_move:
            opponent = 1 if current_player == 2 else 2
            blocking_move = self.find_winning_move(state, opponent)
            if blocking_move:
                best_move = blocking_move
                rationale += f"Blocking opponent's winning move at position {blocking_move}.\n"

        # Check for potential two-way win setup
        if not best_move:
            rationale += "Checking if a two-way win can be set up...\n"
            two_way_win_setup = self.check_potential_two_way_win(state, current_player)
            if two_way_win_setup:
                best_move = two_way_win_setup
                rationale += f"Setting up a two-way win with move at position {best_move}.\n"

        # If no best move is found, fallback to a random move from available options
        if best_move is None:
            rationale += "No immediate winning or blocking move was found. Falling back to a random move based on available options.\n"
            best_move = self.get_random_move(state)

        # Log the decision with the final best move and rationale
        self.log_decision_with_thoughts(step, state, rendered_state, current_player, best_move, rationale, winning_move, blocking_move)

        # Return the best move (or the fallback move if none found)
        return best_move
