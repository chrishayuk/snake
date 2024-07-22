import os
import numpy as np
import random

class MinesweeperEnv:
    def __init__(self, size=10, num_mines=10):
        self.size = size
        self.num_mines = num_mines
        self.reset()

    def reset(self):
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

    def get_state(self):
        state = np.zeros((self.size, self.size, 3), dtype=int)
        state[:,:,0] = self.revealed
        state[:,:,1] = self.flagged
        state[:,:,2] = np.where(self.revealed, self.board, -2)
        return state

    def step(self, action):
        row, col, is_flag = action
        
        if self.game_over:
            return self.get_state(), 0, True

        self.steps += 1

        # New: Add action to history
        action_type = "FLAG" if is_flag else "REVEAL"
        self.action_history.append(f"Step {self.steps}: {action_type} ({row}, {col})")

        print(f"Debug: Action ({row}, {col}), is_flag: {is_flag}")

        reward = 0
        if is_flag:
            if not self.revealed[row, col]:
                self.flagged[row, col] = not self.flagged[row, col]
                print(f"Debug: Toggled flag at ({row}, {col})")
        elif self.flagged[row, col]:
            print(f"Debug: Cell ({row}, {col}) is flagged, can't reveal")
        elif self.revealed[row, col]:
            print(f"Debug: Cell ({row}, {col}) already revealed")
        elif self.board[row, col] == -1:
            self.revealed[row, col] = True
            self.game_over = True
            print(f"Debug: Hit mine at ({row}, {col}). Game over.")
            reward = -10
        else:
            cells_revealed = self.reveal(row, col)
            reward = cells_revealed
            print(f"Debug: Action ({row}, {col}), Cells revealed: {cells_revealed}")

        print(f"Debug: Total revealed: {np.sum(self.revealed)}, Safe cells: {self.size * self.size - self.num_mines}")
        
        # Update game state
        self.update_game_state()
        
        return self.get_state(), reward, self.game_over

    def reveal(self, row, col):
        if self.revealed[row, col] or self.flagged[row, col]:
            return 0
        
        cells_revealed = 1
        self.revealed[row, col] = True
        print(f"Debug: Revealing cell ({row}, {col}), value: {self.board[row, col]}")

        if self.board[row, col] == 0:
            for i in range(max(0, row-1), min(self.size, row+2)):
                for j in range(max(0, col-1), min(self.size, col+2)):
                    if (i, j) != (row, col) and not self.revealed[i, j]:
                        cells_revealed += self.reveal(i, j)
        
        return cells_revealed

    def update_game_state(self):
        safe_cells_revealed = np.sum(self.revealed[self.board != -1])
        total_safe_cells = self.size * self.size - self.num_mines
        
        if safe_cells_revealed >= total_safe_cells:  # Changed from total_safe_cells - 1
            self.win = True
            self.game_over = True
            print(f"Debug: All safe cells revealed. Win! ({safe_cells_revealed}/{total_safe_cells})")
        elif np.sum(self.flagged) == self.num_mines and np.all(self.flagged == (self.board == -1)):
            self.win = True
            self.game_over = True
            print(f"Debug: All mines correctly flagged. Win!")

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

        # Show all actions in the history
        history_str = "\nAction History:\n" + "\n".join(self.action_history)

        render_str = f"{grid_str}\n\n{info_str}\n{history_str}"

        return render_str

    def render(self):
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        print(self.get_render())