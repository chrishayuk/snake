import random
import time
import numpy as np
import math
from collections import defaultdict
from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_classic_agent import BaseTicTacToeClassicAgent


class MonteCarloTreeSearchTicTacToeAgent(BaseTicTacToeClassicAgent):
    def __init__(self, id: str, name: str, description: str, player=2, simulations=10000, exploration_weight=1):
        super().__init__(id, name, description, player)
        self.simulations = simulations  # Number of simulations for MCTS
        self.exploration_weight = exploration_weight  # Exploration constant for UCT
        self.state_visits = defaultdict(int)  # Store visit counts for each state
        self.state_wins = defaultdict(float)  # Store win counts for each state
        self.state_children = {}  # Store the possible actions (children) for each state

    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.CLASSIC

    def get_action(self, step: int, state) -> int:
        """
        Perform MCTS to choose the best action and log the decision.
        """
        for _ in range(self.simulations):
            self.run_simulation(state)

        # Get the best move
        best_move = self.best_action(state)

        # Calculate the best score (win rate) for logging
        best_score = self.state_wins[(state.tostring(), best_move)] / max(self.state_visits[(state.tostring(), best_move)], 1)

        # Log the decision with the logger
        time_of_action = time.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.log_decision(
            game_id=self.game_id,              # The agent's ID, but you can adjust if using a game ID elsewhere
            step=step,                    # Current step in the game
            state=state,                  # Current board state
            thought_process=f"best score was {best_score} for the best move {best_move}",  # Description of the decision-making process
            final_output=best_move,        # The best move chosen by the Minimax algorithm
            response=best_move,            # The best move chosen by the Minimax algorithm
            time_completed=time_of_action # Timestamp of when the action was completed
        )

        # Return the best move
        return best_move


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
