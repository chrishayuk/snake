import numpy as np
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.base_llm_agent import BaseLLMAgent
from agents.provider_type import ProviderType
from agents.tic_tac_toe.base_tic_tac_toe_agent import BaseTicTacToeAgent
from agents.agent_tag_utils import extract_final_output, extract_thought_process, extract_time_completed

class BaseTicTacToeLLMAgent(BaseLLMAgent, BaseTicTacToeAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, prompt_template: str, player=1):
        super().__init__(id, name, description, provider, model_name, prompt_template)
        
        # set the player, prompt and chain
        self.player = player
        self.prompt = PromptTemplate(input_variables=["state", "player"], template=prompt_template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def parse_state(self, state_str: str) -> np.ndarray:
        """Convert the string representation of the game board back into a 2D NumPy array."""
        # Extract the part of the string that contains the game board
        board_start = state_str.find("Game Board:")
        board_lines = state_str[board_start:].strip().split("\n")[1:4]  # Extract the next 3 lines after "Game Board:"
        
        # Parse the board into a 2D NumPy array where '.' represents an empty space (0)
        board = np.array([[1 if cell == 'X' else 2 if cell == 'O' else 0 for cell in line.split()] for line in board_lines])
        return board

    def get_action(self, step: int, state_str: str) -> int:
        # Parse the state string into a 2D array
        state = self.parse_state(state_str)

        # Get the response from the LLM
        response = self.chain.run(state=state_str, player=self.player)

        # Extract thought process, final output, and time completed from the response
        thought_process = extract_thought_process(response)
        final_output = extract_final_output(response)
        time_completed = extract_time_completed(response)

        # Log the decision
        self.logger.log_decision(self.game_id, step, state_str, thought_process, final_output, response, time_completed, self.llm_provider, self.model_name)

        # Get the action from the final output
        action = int(final_output.strip()) if final_output.strip().isdigit() else None
        available_actions = self.get_available_actions(state)

        # If the action is valid, return it; otherwise, select a random valid move
        if action in available_actions:
            return action
        else:
            random_action = self.get_random_move(state)
            self.logger.log_decision(self.game_id, step, state_str, "failed to get valid response from model, so made random action.", random_action, random_action, time_completed, self.llm_provider, self.model_name)
            return random_action
