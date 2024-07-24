import os
import uuid
import numpy as np
import random
from agents.minesweeper.agent_action import MinesweeperAction
from environments.environment_base import Environment

class MinesweeperEnv(Environment):
    def __init__(self, size=10, num_mines=10):
        self.size = size
        self.num_mines = num_mines
        self.reset()

    def reset(self):
        self.game_id = str(uuid.uuid4())
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.revealed = np.zeros((self.size, self.size), dtype=bool)
        self.flagged = np.zeros((self.size, self.size), dtype=bool)
        self.game_over = False
        self.win = False
        self.steps = 0
        self.action_history = []
        
        self.place_mines()
        self.calculate_numbers()

        return self.get_state()

    def update_game_state(self):
        if self.game_over:
            return

        safe_cells_revealed = np.sum(self.revealed[self.board != -1])
        total_safe_cells = self.size * self.size - self.num_mines
        
        if safe_cells_revealed == total_safe_cells:
            self.win = True
            self.game_over = True
        elif np.sum(self.flagged) == self.num_mines and np.all(self.flagged == (self.board == -1)):
            self.win = True
            self.game_over = True

    def get_state(self):
        state = np.zeros((self.size, self.size, 3), dtype=int)
        state[:,:,0] = self.revealed
        state[:,:,1] = self.flagged
        state[:,:,2] = np.where(self.revealed, self.board, -2)
        return state

    def place_mines(self):
        positions = [(r, c) for r in range(self.size) for c in range(self.size)]
        mine_positions = random.sample(positions, self.num_mines)
        for row, col in mine_positions:
            self.board[row, col] = -1

    def calculate_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] != -1:
                    self.board[i, j] = self.count_adjacent_mines(i, j)

    def count_adjacent_mines(self, row, col):
        count = 0
        for i in range(max(0, row-1), min(self.size, row+2)):
            for j in range(max(0, col-1), min(self.size, col+2)):
                if self.board[i, j] == -1:
                    count += 1
        return count

    def reveal(self, row, col):
        if self.revealed[row, col] or self.flagged[row, col]:
            return 0
        
        cells_revealed = 1
        self.revealed[row, col] = True

        if self.board[row, col] == 0:
            for i in range(max(0, row-1), min(self.size, row+2)):
                for j in range(max(0, col-1), min(self.size, col+2)):
                    if (i, j) != (row, col) and not self.revealed[i, j]:
                        cells_revealed += self.reveal(i, j)
        
        return cells_revealed
    
    def step(self, action: MinesweeperAction):
        if self.game_over:
            return self.get_state(), 0, True

        if action is None:
            self.action_history.append(f"Invalid action: None")
            return self.get_state(), 0, False

        self.steps += 1
        row, col, is_flag = action.row, action.col, action.action_type == MinesweeperAction.ActionType.FLAG
        
        action_type = "FLAG" if is_flag else "REVEAL"
        self.action_history.append(f"Step {self.steps}: {action_type} ({row}, {col})")
        
        reward = 0
        if is_flag:
            if not self.revealed[row, col]:
                self.flagged[row, col] = not self.flagged[row, col]
                reward = 0.5 if self.flagged[row, col] else -0.5
        elif not self.flagged[row, col] and not self.revealed[row, col]:
            if self.board[row, col] == -1:
                self.revealed[row, col] = True
                self.game_over = True
                reward = -10
            else:
                cells_revealed = self.reveal(row, col)
                reward = cells_revealed

        self.update_game_state()
        
        return self.get_state(), reward, self.game_over

    def get_render(self):
        grid = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if self.flagged[i, j]:
                    row.append('F')
                elif not self.revealed[i, j]:
                    row.append('.')
                elif self.board[i, j] == -1:
                    row.append('*')
                elif self.board[i, j] == 0:
                    row.append(' ')
                else:
                    row.append(str(self.board[i, j]))
            grid.append(' '.join(row))

        grid_str = '\n'.join(grid)

        info = [
            f"Game ID: {self.game_id}",
            f"Mines: {self.num_mines}",
            f"Revealed: {np.sum(self.revealed)}",
            f"Flagged: {np.sum(self.flagged)}",
            f"Steps: {self.steps}",
            f"Game over: {self.game_over}",
            f"Win: {self.win}",
            f"Safe cells revealed: {np.sum(self.revealed[self.board != -1])}",
            f"Total safe cells: {self.size * self.size - self.num_mines}"
        ]

        info_str = "\n".join(info)
        history_str = "\nAction History:\n" + "\n".join(self.action_history)
        render_str = f"{grid_str}\n\n{info_str}\n{history_str}"
        return render_str
    
    def render(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.get_render())