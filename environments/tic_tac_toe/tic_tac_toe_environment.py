import os
import uuid
import numpy as np
from datetime import datetime
from environments.environment_base import Environment

class TicTacToeEnv(Environment):
    def __init__(self, player_x_id="PlayerX", player_o_id="PlayerO", player_x_type="AI", player_o_type="AI"):
        # Player information
        self.player_x_id = player_x_id
        self.player_o_id = player_o_id
        self.player_x_type = player_x_type
        self.player_o_type = player_o_type
        
        # Initialize the board (3x3 grid), 0 = empty, 1 = 'X', 2 = 'O'
        self.board = np.zeros((3, 3), dtype=int)
        
        # Current player (1 for 'X', 2 for 'O')
        self.current_player = 1
        
        # Track if the game is over
        self.game_over = False
        
        # Game result message
        self.result_message = "Game is ongoing."
        
        # Steps taken in the game
        self.steps = 0

        # Initialize action history
        self.action_history = []
        
        # Reset the environment at initialization
        self.reset()

    def reset(self):
        # Set the game_id and start time
        self.game_id = str(uuid.uuid4())
        self.game_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.game_end_time = None

        # Reset the board and game status
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.steps = 0
        self.result_message = "Game is ongoing."
        self.action_history = []
        self.game_end_time = None

        # get the state
        return self.get_state()

    def get_state(self):
        # Return the current board state
        return np.copy(self.board)

    def step(self, action):
        """
        Take a step in the environment. The action is expected to be a number from 1 to 9,
        representing the position where the current player wants to place their mark.
        """
        if self.game_over:
            raise ValueError("Game is over. Please reset the environment.")

        # Convert the action (1-9) into row, col coordinates
        action_map = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 9: (2, 2)
        }

        if action not in action_map:
            raise ValueError(f"Invalid action: {action} is not a valid move (1-9).")

        row, col = action_map[action]

        if self.board[row, col] != 0:
            raise ValueError(f"Invalid action: Cell ({row}, {col}) is already occupied.")

        # Log the action to the action history
        self.action_history.append({
            "step": self.steps + 1,
            "player": 'X' if self.current_player == 1 else 'O',
            "action": action  # Log the number instead of tuple
        })

        # Place the player's mark
        self.board[row, col] = self.current_player
        self.steps += 1

        # Check if the current player wins
        if self.check_win(self.current_player):
            self.game_over = True
            self.result_message = f"Player {'X' if self.current_player == 1 else 'O'} wins!"
            self.game_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return self.get_state(), 1 if self.current_player == 1 else -1, self.game_over

        # Check for draw
        if self.steps == 9:
            self.game_over = True
            self.result_message = "The game is a draw."
            self.game_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return self.get_state(), 0, self.game_over  # Draw

        # Render before switching player
        self.render()

        # Switch to the next player
        self.current_player = 2 if self.current_player == 1 else 1

        # No win or draw, return neutral reward
        return self.get_state(), 0, self.game_over


    def check_win(self, player):
        """
        Check if the given player has won the game.
        """
        # Check rows, columns, and diagonals for a win
        return (
            np.any(np.all(self.board == player, axis=0)) or  # Check columns
            np.any(np.all(self.board == player, axis=1)) or  # Check rows
            np.all(np.diag(self.board) == player) or  # Check main diagonal
            np.all(np.diag(np.fliplr(self.board)) == player)  # Check anti-diagonal
        )

    def get_render(self):
        render_str = "\n"
        symbols = {0: '.', 1: 'X', 2: 'O'}
        
        # Add Game Board Header
        render_str += "Game Board:\n"
        
        # Add board display
        for row in self.board:
            render_str += " ".join([symbols[cell] for cell in row]) + "\n"

        render_str += "\n"
        
        # Add Game Instructions for simpler move system
        instructions = [
            "Game Instructions:",
            "-" * 35,
            "1. The game is played on a 3x3 grid.",
            "2. Player X always goes first, followed by Player O.",
            "3. Players take turns placing their mark (X or O) in an empty cell.",
            "4. To make a move, select a number from 1 to 9 corresponding to the position on the grid:",
            "   1 | 2 | 3",
            "   4 | 5 | 6",
            "   7 | 8 | 9",
            "5. The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins.",
            "6. If all 9 cells are filled and no player has 3 in a row, the game is a draw.",
            "-" * 35,
        ]

        # Game details
        game_state = [
            "Game Information:",
            "-" * 35,
            f" Game ID         : {self.game_id}",
            f" Game Start Time : {self.game_start_time}",
            f" Game End Time   : {self.game_end_time if self.game_end_time else 'Ongoing'}",
            f" Current Player  : {'X' if self.current_player == 1 else 'O'}",
            f" Steps Taken     : {self.steps}",
            f" Game Over       : {self.game_over}",
            f" Result          : {self.result_message}",
            "-" * 35,
        ]
        
        # Player information
        player_info = [
            "Players:",
            "-" * 35,
            f" Player X ID : {self.player_x_id} (Type: {self.player_x_type})",
            f" Player O ID : {self.player_o_id} (Type: {self.player_o_type})",
            "-" * 35,
        ]
        
        # Legend
        legend = [
            "Legend:",
            "-" * 35,
            " X - Player X's mark",
            " O - Player O's mark",
            " . - Empty space",
            "-" * 35,
        ]
        
        # Action history
        action_history_str = "\nAction History:\n" + "-" * 35 + "\n"
        if self.action_history:
            for record in self.action_history:
                action_history_str += f" Step {record['step']} : {record['player']} placed mark at {record['action']}\n"
        else:
            action_history_str += " No actions have been made yet."
        
        action_history_str += "-" * 35
        
        # Combine all elements
        render_str += "\n".join(instructions) + "\n\n" + "\n".join(game_state) + "\n\n" + "\n".join(player_info) + "\n\n" + "\n".join(legend) + "\n" + action_history_str
        
        return render_str




    def render(self):
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get and print the render string
        print(self.get_render())

    def get_action_history(self):
        """
        Returns the action history as a list of dictionaries.
        """
        return self.action_history
