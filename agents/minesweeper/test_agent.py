import random
from .agent_action import MinesweeperAction

class TestAgent:
    def __init__(self, size):
        self.size = size
        self.reset()

    def reset(self):
        self.unrevealed = set((i, j) for i in range(self.size) for j in range(self.size))
        self.flagged = set()
        self.visited = set()  # Track visited actions

    def get_action(self, state):
        revealed = state[:,:,0]
        flagged = state[:,:,1]
        board = state[:,:,2]

        print(f"Debug: Unrevealed cells: {len(self.unrevealed)}")
        print(f"Debug: Flagged cells: {len(self.flagged)}")

        # First, try to find a safe move
        for i in range(self.size):
            for j in range(self.size):
                if revealed[i, j] and board[i, j] > 0:
                    adjacent = self.get_adjacent(i, j)
                    unrevealed = [pos for pos in adjacent if pos in self.unrevealed]
                    adjacent_flags = sum(1 for pos in adjacent if pos in self.flagged)
                    
                    if len(unrevealed) + adjacent_flags == board[i, j]:
                        # All unrevealed adjacent cells are mines, flag them
                        for pos in unrevealed:
                            if pos not in self.flagged and pos not in self.visited:
                                self.visited.add(pos)
                                print(f"Debug: Flagging cell {pos}")
                                return MinesweeperAction(MinesweeperAction.ActionType.FLAG, pos[0], pos[1])
                    elif len(unrevealed) > board[i, j] - adjacent_flags:
                        # There are safe cells to reveal
                        safe = [pos for pos in unrevealed if pos not in self.flagged and pos not in self.visited]
                        if safe:
                            self.visited.add(safe[0])
                            print(f"Debug: Revealing safe cell {safe[0]}")
                            return MinesweeperAction(MinesweeperAction.ActionType.REVEAL, safe[0][0], safe[0][1])

        # If no safe move found, choose a random unrevealed cell
        unrevealed_unflagged = list(self.unrevealed - self.flagged - self.visited)
        if unrevealed_unflagged:
            i, j = random.choice(unrevealed_unflagged)
            self.visited.add((i, j))
            print(f"Debug: Revealing random cell ({i}, {j})")
            return MinesweeperAction(MinesweeperAction.ActionType.REVEAL, i, j)

        # If all cells are revealed or flagged, we're done
        print("Debug: No more moves available")
        return None

    def get_adjacent(self, i, j):
        adjacent = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < self.size and 0 <= nj < self.size:
                    adjacent.append((ni, nj))
        return adjacent

    def update(self, action, revealed):
        if action.action_type == MinesweeperAction.ActionType.REVEAL:
            self.unrevealed.discard((action.row, action.col))
        elif action.action_type == MinesweeperAction.ActionType.FLAG:
            self.flagged.add((action.row, action.col))
        for i, j in revealed:
            self.unrevealed.discard((i, j))
        
        print(f"Debug: After update - Unrevealed: {len(self.unrevealed)}, Flagged: {len(self.flagged)}")
