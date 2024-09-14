import random
import numpy as np
import math
from agents.base_agent import BaseAgent
from collections import defaultdict

class MonteCarloTreeSearchTicTacToeAgent(BaseAgent):
    def __init__(self, id: str, name: str, description: str, player=2, simulations=10000, exploration_weight=1):
        super().__init__(id, name, description)
        self.player = player  # The agent's player (1 for 'X' or 2 for 'O')
        self.simulations = simulations  # Number of simulations for MCTS
        self.exploration_weight = exploration_weight  # Exploration constant for UCT
        self.state_visits = defaultdict(int)  # Store visit counts for each state
        self.state_wins = defaultdict(float)  # Store win counts for each state
        self.state_children = {}  # Store the possible actions (children) for each state

    @property
    def agent_type(self) -> str:
        """Return the type of the agent."""
        return "Monte Carlo Tree Search Tic-Tac-Toe"

    def get_action(self, step: int, state) -> int:
        """
        Perform MCTS to choose the best action.
        """
        for _ in range(self.simulations):
            self.run_simulation(state)
        
        # Select the move with the highest win rate
        return self.best_action(state)

    def run_simulation(self, state):
        """
        Run a single MCTS simulation: Selection, Expansion, Simulation, and Backpropagation.
        """
        path = []
        current_player = self.player
        state_copy = np.copy(state)
        
        # Selection: Traverse the tree based on UCB until we reach an unexplored state
        while self.is_fully_expanded(state_copy) and state_copy.tostring() in self.state_children:
            action, state_copy = self.select(state_copy)
            path.append((state_copy.tostring(), action))
            current_player = 2 if current_player == 1 else 1  # Switch player
        
        # Expansion: Add new child states to the tree if we encounter an unexplored state
        if not self.is_terminal(state_copy):
            action = self.expand(state_copy, current_player)
            state_copy = self.apply_action(state_copy, action, current_player)
            path.append((state_copy.tostring(), action))
        
        # Simulation: Play out the game randomly from the new state
        winner = self.simulate_game(state_copy, current_player)
        
        # Backpropagation: Update the nodes in the path with the result of the simulation
        self.backpropagate(path, winner)

    def is_fully_expanded(self, state) -> bool:
        """Check if all possible actions have been explored from this state."""
        return state.tostring() in self.state_children and len(self.state_children[state.tostring()]) == len(self.get_available_actions(state))

    def select(self, state):
        """Use Upper Confidence Bound (UCB) to select the best child."""
        best_ucb = -float('inf')
        best_action = None
        best_state = None
        total_visits = sum(self.state_visits[(state.tostring(), action)] for action in self.state_children[state.tostring()])

        for action in self.state_children[state.tostring()]:
            state_after_action = self.apply_action(state, action, self.player)
            visits = self.state_visits[(state.tostring(), action)]
            wins = self.state_wins[(state.tostring(), action)]
            
            if visits == 0:
                # Assign a large UCB value to encourage exploration
                ucb = float('inf')
            else:
                # Calculate UCB normally
                ucb = (wins / visits) + self.exploration_weight * math.sqrt(math.log(total_visits) / visits)

            if ucb > best_ucb:
                best_ucb = ucb
                best_action = action
                best_state = state_after_action

        return best_action, best_state


    def expand(self, state, current_player):
        """Add unexplored actions to the tree."""
        available_actions = self.get_available_actions(state)
        if state.tostring() not in self.state_children:
            self.state_children[state.tostring()] = available_actions
        
        return random.choice(available_actions)

    def simulate_game(self, state, current_player):
        """Simulate the game randomly from the given state."""
        while not self.is_terminal(state):
            available_actions = self.get_available_actions(state)
            action = random.choice(available_actions)
            state = self.apply_action(state, action, current_player)
            current_player = 2 if current_player == 1 else 1
        
        # Return the winner (1 for X, 2 for O, 0 for draw)
        return self.get_winner(state)

    def backpropagate(self, path, winner):
        """Backpropagate the result of the simulation up the tree."""
        for state_str, action in path:
            self.state_visits[(state_str, action)] += 1
            if winner == self.player:
                self.state_wins[(state_str, action)] += 1

    def best_action(self, state) -> int:
        """Return the action with the highest win rate."""
        best_action = None
        best_win_rate = -float('inf')

        for action in self.get_available_actions(state):
            state_after_action = self.apply_action(state, action, self.player)
            visits = self.state_visits[(state.tostring(), action)]
            wins = self.state_wins[(state.tostring(), action)]
            win_rate = wins / visits if visits > 0 else 0
            
            if win_rate > best_win_rate:
                best_win_rate = win_rate
                best_action = action
        
        return best_action

    def get_available_actions(self, state) -> list:
        """Return the list of available actions (1-9) based on the current board state."""
        action_map = {
            (0, 0): 1, (0, 1): 2, (0, 2): 3,
            (1, 0): 4, (1, 1): 5, (1, 2): 6,
            (2, 0): 7, (2, 1): 8, (2, 2): 9
        }
        empty_positions = [(r, c) for r in range(3) for c in range(3) if state[r, c] == 0]
        return [action_map[(r, c)] for (r, c) in empty_positions]

    def apply_action(self, state, action, player):
        """Apply an action to the board and return the resulting state."""
        action_map = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 9: (2, 2)
        }
        row, col = action_map[action]
        new_state = np.copy(state)
        new_state[row, col] = player
        return new_state

    def is_terminal(self, state) -> bool:
        """Check if the game has reached a terminal state (win or draw)."""
        return self.get_winner(state) is not None or not np.any(state == 0)

    def get_winner(self, state):
        """Check for a winner. Return 1 for X, 2 for O, or 0 for draw."""
        for player in [1, 2]:
            if (
                any(np.all(state[row, :] == player) for row in range(3)) or
                any(np.all(state[:, col] == player) for col in range(3)) or
                np.all(np.diag(state) == player) or
                np.all(np.diag(np.fliplr(state)) == player)
            ):
                return player
        if not np.any(state == 0):
            return 0  # Draw
        return None
