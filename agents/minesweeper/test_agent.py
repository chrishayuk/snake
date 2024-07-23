import random
import time
from agents.agent_type import AgentType
from agents.base_agent import BaseAgent
from .agent_action import MinesweeperAction

class TestAgent(BaseAgent):
    def __init__(self, id: str, name: str, description: str, size):
        """Initialize the TestAgent with the given parameters."""
        super().__init__(id, name, description)

        # set the size of the game
        self.size = size

        # reset the game
        self.reset()

    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC

    def reset(self):
        """Reset the agent's state for a new game."""
        self.unrevealed = set((i, j) for i in range(self.size) for j in range(self.size))
        self.flagged = set()
        self.visited = set()

    def get_action(self, state):
        """ Determine the next action for the agent based on the current game state. """
        revealed = state[:, :, 0]
        flagged = state[:, :, 1]
        board = state[:, :, 2]
        best_move = None  # Initialize the best_move variable
        start_time = time.time()  # Start time for measuring decision time

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
                                best_move = MinesweeperAction(MinesweeperAction.ActionType.FLAG, pos[0], pos[1])
                                break
                    elif len(unrevealed) > board[i, j] - adjacent_flags:
                        # There are safe cells to reveal
                        safe = [pos for pos in unrevealed if pos not in self.flagged and pos not in self.visited]
                        if safe:
                            self.visited.add(safe[0])
                            best_move = MinesweeperAction(MinesweeperAction.ActionType.REVEAL, safe[0][0], safe[0][1])
                            break
                if best_move:
                    break
            if best_move:
                break

        # If no safe move found, choose a random unrevealed cell
        if not best_move:
            unrevealed_unflagged = list(self.unrevealed - self.flagged - self.visited)
            if unrevealed_unflagged:
                i, j = random.choice(unrevealed_unflagged)
                self.visited.add((i, j))
                best_move = MinesweeperAction(MinesweeperAction.ActionType.REVEAL, i, j)

        # If all cells are revealed or flagged, we're done
        if not best_move:
            return None

        # Log the state, thought process, and decision
        thought_process = "Determined best move based on current board state."
        time_completed = time.time() - start_time  # Measure the time taken to decide
        self.logger.log_decision(self.game_id, state, thought_process, str(best_move), str(best_move), time_completed)

        return best_move

    def get_adjacent(self, i, j):
        """ Get the adjacent cells for a given cell. """
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
        """ Update the agent's state based on the latest action and revealed cells. """
        if action.action_type == MinesweeperAction.ActionType.REVEAL:
            self.unrevealed.discard((action.row, action.col))
        elif action.action_type == MinesweeperAction.ActionType.FLAG:
            self.flagged.add((action.row, action.col))

        # loop through revealed
        for i, j in revealed:
            self.unrevealed.discard((i, j))
