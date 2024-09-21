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
        
        # set the player, prompt, and chain
        self.player = player  # Player assignment (e.g., 1 for X, 2 for O)
        self.prompt = PromptTemplate(input_variables=["state", "player"], template=prompt_template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def parse_state(self, state_str: str) -> np.ndarray:
        """Convert the string representation of the game board back into a 2D NumPy array."""
        try:
            # Extract the part of the string that contains the game board
            board_start = state_str.find("Game Board:")
            board_lines = state_str[board_start:].strip().split("\n")[1:4]  # Extract the next 3 lines after "Game Board:"

            # Parse the board into a 2D NumPy array where '.' represents an empty space (0)
            board = np.array([[1 if cell == 'X' else 2 if cell == 'O' else 0 for cell in line.split()] for line in board_lines])
            return board
        except Exception as e:
            print(f"Error parsing state: {e}")
            return np.zeros((3, 3), dtype=int)  # Return empty board on error

    def get_action(self, step: int, state: np.ndarray, rendered_state: str, current_player: int) -> int:
        """
        Get an action from the LLM or fallback to a random valid action if the LLM response is invalid.
        - state: The current game board as a 2D NumPy array.
        - rendered_state: The visual string representation of the game board.
        - current_player: The player making the move (1 for X, 2 for O).
        """
        # Get the response from the LLM using the rendered state
        try:
            response = self.chain.run(state=rendered_state, player=current_player)
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            response = ""

        # Extract thought process, final output, and time completed from the response
        thought_process = extract_thought_process(response) if response else "LLM failed to generate response."
        final_output = extract_final_output(response) if response else ""
        time_completed = extract_time_completed(response) if response else time.strftime('%Y-%m-%d %H:%M:%S')

        # Get available actions from the state
        available_actions = self.get_available_actions(state)

        # Check if the final output is valid
        action = int(final_output.strip()) if final_output.strip().isdigit() else None
        if action in available_actions:
            # Log the valid LLM-generated action
            self.logger.log_decision(
                game_id=self.game_id,
                step=step,
                state=state,  # Serialize NumPy array to list for logging
                rendered_state=rendered_state,      # Log visual board state
                thought_process=thought_process,
                final_output=action,
                response=final_output,
                time_completed=time_completed,
                provider=self.llm_provider, 
                model=self.model_name, 
                player='X' if current_player == 1 else 'O'
            )
            return action
        else:
            # Fallback to a random valid move
            random_action = self.get_random_move(state)
            thought_process += " | Failed to get valid response from LLM, so made a random action."

            # Log the fallback move
            self.logger.log_decision(
                game_id=self.game_id,
                step=step,
                state=state,
                rendered_state=rendered_state,
                thought_process=thought_process,
                final_output=random_action,
                response=random_action,
                time_completed=time_completed,
                provider=self.llm_provider, 
                model=self.model_name, 
                player='X' if current_player == 1 else 'O'
            )
            return random_action
