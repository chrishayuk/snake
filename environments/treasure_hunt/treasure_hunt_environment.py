import os
import uuid
import numpy as np
import random
from agents.treasure_hunt.llm_agent import TreasureHuntAction
from environments.environment_base import Environment

class TreasureHuntEnv(Environment):
    def __init__(self, size=5):
        self.size = size
        self.reset()

    def reset(self):
        self.game_id = str(uuid.uuid4())
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.guesses = np.zeros((self.size, self.size), dtype=bool)
        self.treasure_found = False
        self.steps = 0
        self.action_history = []

        self.place_treasure()

        return self.get_state()

    def place_treasure(self):
        treasure_row = random.randint(0, self.size - 1)
        treasure_col = random.randint(0, self.size - 1)
        self.treasure_pos = (treasure_row, treasure_col)
        self.board[treasure_row, treasure_col] = 1

    def get_state(self):
        state = np.zeros((self.size, self.size, 2), dtype=int)
        state[:,:,0] = self.guesses
        state[:,:,1] = self.board
        return state

    def provide_feedback(self, row, col):
        treasure_row, treasure_col = self.treasure_pos
        if row == treasure_row and col == treasure_col:
            return "Congratulations! You found the treasure."
        
        if row < treasure_row:
            return "The treasure is to the South."
        elif row > treasure_row:
            return "The treasure is to the North."
        elif col < treasure_col:
            return "The treasure is to the East."
        elif col > treasure_col:
            return "The treasure is to the West."

    def step(self, action):
        if self.treasure_found:
            return self.get_state(), "Game Over: Treasure already found", True

        if action is None or not isinstance(action, TreasureHuntAction):
            self.action_history.append(f"Invalid action: {action}")
            return self.get_state(), "Invalid action", False

        row, col = action.row, action.col

        # Validate coordinates
        if not (0 <= row < self.size and 0 <= col < self.size):
            self.action_history.append(f"Invalid coordinates: ({row}, {col})")
            return self.get_state(), "Invalid coordinates", False

        self.steps += 1
        self.action_history.append(f"Step {self.steps}: GUESS ({row}, {col})")
        
        if self.guesses[row, col]:
            return self.get_state(), "Cell already guessed", False
        
        self.guesses[row, col] = True

        if self.board[row, col] == 1:
            self.treasure_found = True
            feedback = "Congratulations! You found the treasure."
        else:
            feedback = self.provide_feedback(row, col)

        self.action_history[-1] += f" - {feedback}"  # Append feedback to action history
        return self.get_state(), feedback, self.treasure_found

    def get_render(self):
        grid = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if self.guesses[i, j]:
                    if self.board[i, j] == 1:
                        row.append('T')
                    else:
                        row.append('X')
                else:
                    row.append('.')
            grid.append(' '.join(row))

        grid_str = '\n'.join(grid)

        info = [
            f"Game ID: {self.game_id}",
            f"Treasure Found: {self.treasure_found}",
            f"Steps: {self.steps}"
        ]

        info_str = "\n".join(info)
        history_str = "\nAction History:\n" + "\n".join(self.action_history)
        render_str = f"{grid_str}\n\n{info_str}\n{history_str}"
        return render_str
    
    def render(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.get_render())
