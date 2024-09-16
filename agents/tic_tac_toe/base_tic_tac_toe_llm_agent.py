# File: agents/tic_tac_toe/base_llm_tictactoe_agent.py
import random
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.base_llm_agent import BaseLLMAgent
from agents.provider_type import ProviderType
from agents.tic_tac_toe.tic_tac_toe_action import TicTacToeAction
from agents.agent_tag_utils import extract_final_output, extract_thought_process, extract_time_completed
import time

class BaseTicTacToeLLMAgent(BaseLLMAgent):
    action_map = {
        (0, 0): 1, (0, 1): 2, (0, 2): 3,
        (1, 0): 4, (1, 1): 5, (1, 2): 6,
        (2, 0): 7, (2, 1): 8, (2, 2): 9
    }

    reverse_action_map = {v: k for k, v in action_map.items()}  # Reverse map for action to (row, col)

    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, prompt_template: str, player=1):
        # Call the parent constructor
        super().__init__(id, name, description, provider, model_name, prompt_template)

        # set the player
        self.player = player  # The agent's player (1 for 'X' or 2 for 'O')

        # Update the prompt to include the state and other relevant variables
        self.prompt = PromptTemplate(input_variables=["state", "player"], template=prompt_template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def get_available_actions(self, state: str) -> list:
        """Extract the game board from the state string and return the available actions (1-9)."""
        # Extract the part of the string that contains the game board
        board_start = state.find("Game Board:")
        board_lines = state[board_start:].strip().split("\n")[1:4]  # Extract the next 3 lines after "Game Board:"

        # Parse the board into a 2D list by removing extra spaces
        board = [line.split() for line in board_lines]

        # Find empty positions (represented by ".")
        empty_positions = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '.']

        # Return the corresponding actions (1-9) for the empty positions
        return [self.action_map[(r, c)] for r, c in empty_positions]

    def get_random_move(self, state: str) -> int:
        """Extract the game board from the state string and return a random valid move (1-9)."""
        # Extract the part of the string that contains the game board
        board_start = state.find("Game Board:")
        board_lines = state[board_start:].strip().split("\n")[1:4]  # Extract the next 3 lines after "Game Board:"

        # Parse the board into a 2D list by removing extra spaces
        board = [line.split() for line in board_lines]

        # Find empty positions (represented by ".")
        empty_positions = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '.']

        if empty_positions:
            row, col = random.choice(empty_positions)
            return self.action_map[(row, col)]
        return None

    def get_action(self, step: int, state) -> int:
        # Get the response from the LLM
        response = self.chain.run(state=state, player=self.player)

        # Extract the necessary tags from the response
        thought_process = extract_thought_process(response)
        final_output = extract_final_output(response)
        time_completed = extract_time_completed(response)

        # Log the decision
        self.logger.log_decision(self.game_id, step, state, thought_process, final_output, response, time_completed, self.llm_provider, self.model_name)

        # Map the final output to an integer (1 to 9)
        action = int(final_output.strip()) if final_output.strip().isdigit() else None

        # Get available actions from the current state
        available_actions = self.get_available_actions(state)

        # If the action is valid, return it; otherwise, select a random valid move
        if action in available_actions:
            return action
        else:
            random_action = self.get_random_move(state)
            self.logger.log_decision(self.game_id, step, state, "failed to get valid response from model, so made random action.", random_action, random_action, time_completed, self.llm_provider, self.model_name)
            return random_action


    def game_over(self, step: int, state: str):
        # Call the parent method to handle game over logic
        super().game_over(step, state)
