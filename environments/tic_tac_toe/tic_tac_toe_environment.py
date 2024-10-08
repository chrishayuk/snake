import os
import uuid
import numpy as np
import logging
from datetime import datetime
from environments.environment_base import Environment
from environments.tic_tac_toe.action_history import ActionHistory
from environments.tic_tac_toe.reward_functions import simple_reward

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TicTacToeEnv(Environment):
    def __init__(self, player_x_id="PlayerX", player_o_id="PlayerO", player_x_type="AI", player_o_type="AI", reward_function=simple_reward):
        # Player information
        self.player_x_id = player_x_id
        self.player_o_id = player_o_id
        self.player_x_type = player_x_type
        self.player_o_type = player_o_type
        
        # Initialize the board (3x3 grid), 0 = empty, 1 = 'X', 2 = 'O'
        self.board = np.zeros((3, 3), dtype=int)
        
        # Current player (1 for 'X', 2 for 'O')
        self.current_player = 1

        # Reward function
        self.reward_function = reward_function
        
        # Track if the game is over
        self.game_over = False
        
        # Game result message
        self.result_message = "Game is ongoing."
        
        # Steps taken in the game
        self.steps = 0

        # Action history (newly added)
        self.action_history = ActionHistory()

        # Swap players flag
        self.swap_players = False  # Initialize swapping flag
        
        # Agents list
        self.original_agents = []  # Preserve original agent order
        self.agents = []  # Current agent order

        # Reset the environment at initialization
        self.reset()

    def set_agents(self, agents):
        """
        Set agent names and types for Player X and Player O based on the passed list.
        Preserves the original agent order.
        """
        self.original_agents = agents.copy()  # Preserve original order
        self.agents = agents.copy()  # Set current agents

        # Ensure this is a 2-player game
        if len(self.agents) == 2:
            # Assign Player X (agent[0]) and Player O (agent[1])
            self.agents[0].player = 1  # Player X
            self.agents[1].player = 2  # Player O

            # Set the id and type for Player X, as the first agent
            self.player_x_id = self.agents[0].name  
            self.player_x_type = getattr(self.agents[0], 'agent_type', "Unknown")

            # Set the id and type for Player O, as the second agent
            self.player_o_id = self.agents[1].name
            self.player_o_type = getattr(self.agents[1], 'agent_type', "Unknown")

            # Log the setting of the agents
            logger.info(f"Agents set: Player X -> {self.player_x_id}, Player O -> {self.player_o_id}")
        else:
            # Not enough agents
            logger.warning("Insufficient agents to set Player X and Player O.")


    def reset(self):
        """
        Reset the environment for a new episode. Handles player swapping based on the swap_players flag.
        """
        # Set the game_id and start time
        self.game_id = str(uuid.uuid4())  # Ensure game_id is regenerated every reset
        self.game_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.game_end_time = None

        # Reset the board and game status
        self.board = np.zeros((3, 3), dtype=int)
        self.game_over = False
        self.steps = 0
        self.result_message = "Game is ongoing."

        # Reset the action history
        self.action_history.clear()

        # Swap players if flag is set, otherwise keep original order
        if self.swap_players and len(self.original_agents) >= 2:
            self.agents = [self.original_agents[1], self.original_agents[0]]  # Swap agents
        else:
            self.agents = self.original_agents.copy()

        # Update player IDs and types for Player X and Player O
        if len(self.agents) >= 2:
            self.agents[0].player = 1  # Player X
            self.agents[1].player = 2  # Player O
            self.player_x_id = self.agents[0].name
            self.player_x_type = getattr(self.agents[0], 'agent_type', "Unknown")
            self.player_x_unique_agent_id = self.agents[0].unique_agent_id
            self.player_o_id = self.agents[1].name
            self.player_o_type = getattr(self.agents[1], 'agent_type', "Unknown")
            self.player_o_unique_agent_id = self.agents[1].unique_agent_id

        # Toggle the swap_players flag for the next game
        self.swap_players = not self.swap_players

        # Assign the new game_id to each agent
        for agent in self.agents:
            agent.game_id = self.game_id

        # Set the current player to Player X
        self.current_player = 1  # Player X always starts

        # Return the current state of the board
        return self.get_state()


    def step(self, action, agent=None):
        """
        Take a step in the environment. The action is expected to be a number from 1 to 9,
        representing the position where the current player wants to place their mark.
        """
        # Check if the game is over
        if self.game_over:
            raise ValueError("Game is over. Please reset the environment.")

        # Validate that the correct agent is taking their turn
        if agent:
            if agent.player != self.current_player:
                raise ValueError(f"It is not agent {agent.name}'s turn to play. It is player {self.current_player}'s turn.")

                # Log the invalid turn attempt
                logger.warning(f"Agent {agent.name} tried to make a move when it is Player {self.current_player}'s turn.")


        # Check the move is valid
        if action not in range(1, 10):
            raise ValueError(f"Invalid move: {action}. Must be between 1 and 9.")

        # Convert the action (1-9) into row, col coordinates
        action_map = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 9: (2, 2)
        }

        # Check the move is valid
        row, col = action_map[action]
        if self.board[row, col] != 0:
            raise ValueError(f"Invalid action: Cell ({row}, {col}) is already occupied.")

        # Place the player's mark
        self.board[row, col] = self.current_player
        self.steps += 1

        # Determine the current player role ('X' or 'O')
        player_role = 'X' if self.current_player == 1 else 'O'

        # Add action to action history
        self.action_history.add_record(
            step=self.steps,
            player=player_role,
            action=action
        )

        # Check if the current player wins
        if self.check_win(self.current_player):
            self.game_over = True
            self.result_message = f"Player {player_role} wins!"
            self.game_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Assign reward based on the win and update agent reward
            reward = self.reward_function(won=True, draw=False, ongoing=False)
            if agent:
                agent.add_reward(reward)

            # Return the state, reward, and game over status
            return self.get_state(), reward, self.game_over

        # Check for draw
        if self.steps == 9:
            self.game_over = True
            self.result_message = "The game is a draw."
            self.game_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Assign reward based on the draw and update agent reward
            reward = self.reward_function(won=False, draw=True, ongoing=False)
            if agent:
                agent.add_reward(reward)

            # Return the state, reward, and game over status
            return self.get_state(), reward, self.game_over

        # If game is ongoing, return neutral reward and update agent reward
        reward = self.reward_function(won=False, draw=False, ongoing=True)

        # add the reward
        if agent:
            agent.add_reward(reward)

        # Render before switching player
        self.render()

        # Switch to the next player
        self.current_player = 2 if self.current_player == 1 else 1

        # Return state, reward, and game_over flag
        return self.get_state(), reward, self.game_over


    def get_state(self):
        # Return the current board state
        return np.copy(self.board)
    
    def get_valid_moves(self):
        """Return a list of valid moves (empty cells) from the current board state."""
        return [i+1 for i, cell in enumerate(self.board.flatten()) if cell == 0]

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

    def render(self):
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get and print the render string
        print(self.get_render())

    def get_render(self):
        render_str = "\n"
        symbols = {0: '.', 1: 'X', 2: 'O'}
        
        # Add Game Board Header
        render_str += "Game Board:\n"
        
        # Add board display
        for row in self.board:
            render_str += " ".join([symbols[cell] for cell in row]) + "\n"

        render_str += "\n"
        
        # Add Game Instructions
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
            f" Player X (ID: {self.player_x_id}) Type: {self.player_x_type}",
            f" Player O (ID: {self.player_o_id}) Type: {self.player_o_type}",
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
            for record in self.get_action_history():
                action_history_str += f" Step {record['step']} : {record['player']} placed mark at {record['action']}\n"
        else:
            action_history_str += " No actions have been made yet."
        
        action_history_str += "-" * 35
        
        # Combine all elements
        render_str += "\n".join(instructions) + "\n\n" + "\n".join(game_state) + "\n\n" + "\n".join(player_info) + "\n\n" + "\n".join(legend) + "\n" + action_history_str
        
        return render_str


    def get_action_history(self):
        """Return the full action history."""
        return self.action_history.get_history()
