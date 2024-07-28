# File: agents/snake/llm_agent.py
from agents.agent_tag_utils import extract_final_output, extract_thought_process, extract_time_completed
from agents.provider_type import ProviderType
from agents.base_llm_agent import BaseLLMAgent
from agents.snake.snake_action import SnakeAction
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class LLMAgent(BaseLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str):
        prompt_template = """
You are an AI controlling a snake in a classic Snake game. The game is played on a rectangular grid.

Grid Information:
Size: 10 x 10
Zero-based coordinate system
Top-left coordinate: [0, 0]
Bottom-right coordinate: [9, 9]
Coordinates format: [row_number, column_number]
Moving UP decreases column_number by 1.
Moving DOWN increases column_number by 1.
Moving LEFT decreases row_number by 1.
Moving RIGHT increases row_number by 1.
Grid Symbols:
H: Head of the snake (current position)
O: Body of the snake
F: Food that the snake should eat
.: Empty square
Current Game State:
{state}

Snake Game Strategy:
Primary Goal: Move towards the food (F) to grow the snake.
Avoid Collisions: Ensure the snake does not move into walls or its own body (O).
Plan Ahead: Consider the snake's length and future positions when moving towards food.
Use Space Efficiently: Move in a way that maximizes open paths and avoids tight spaces.
Follow the Tail: In tight spaces, follow the snake's tail to maximize survival.
Maximize Empty Space: If no clear path to food exists, move to maximize empty space around the head.
Decision-Making Process:
Immediate Survival:

Check if the next move will lead to a collision with the wall or the snake's body.
Prioritize moves that avoid immediate danger.
Moving Towards Food:

Calculate the Manhattan distance to the food for all valid moves.
Prefer moves that reduce the distance to the food.
Long-term Survival:

Evaluate the available space around the snake's head after each potential move.
Choose moves that leave the snake with more open paths to navigate.
Avoiding Backtracking:

Avoid moves that would reverse the snake's direction unless there is no other safe option.
Steps to Improve:
Check for all valid moves (UP, DOWN, LEFT, RIGHT):
A move is valid if it does not lead to a collision with the wall or the snake's body.
If only one move is valid, choose that move:
This ensures immediate survival.
If multiple moves are valid, prioritize by:
Manhattan distance to food: Moves that reduce the distance to the food.
Open space evaluation: Moves that leave more open paths for future navigation.
Avoid backtracking: Avoid reversing direction unless it's the only safe option.
Provide your answer as a single word (UP, DOWN, LEFT, or RIGHT) with no additional explanation.
"""
            
        # call the parent
        super().__init__(id, name, description, provider, model_name, prompt_template)

        # update the prompt template to CoT version
        self.prompt_template = prompt_template

        # set the prompt template
        self.prompt = PromptTemplate(input_variables=["state"], template=prompt_template)
        
        # setup the chain with the prompt and llm
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def get_action(self, step: int, state: str):
        # call the llm
        response = self.chain.run(state=state)

        # extract the thought process and final output
        thought_process = extract_thought_process(response)
        final_output = extract_final_output(response)
        time_completed = extract_time_completed(response)

        # log the state, thought process, and decision
        self.logger.log_decision(self.game_id, step, state, thought_process, final_output, response, time_completed)

        # map the action
        action_map = {
            "UP": SnakeAction(SnakeAction.UP),
            "DOWN": SnakeAction(SnakeAction.DOWN),
            "LEFT": SnakeAction(SnakeAction.LEFT),
            "RIGHT": SnakeAction(SnakeAction.RIGHT)
        }

        # ensure the final output is in uppercase and stripped of extra whitespace
        final_output_cleaned = final_output.strip().upper()
        print(f"Final Output Cleaned: {final_output_cleaned}")

        # return the action, default to SnakeAction.RIGHT if invalid
        action = action_map.get(final_output_cleaned, SnakeAction(SnakeAction.RIGHT))
        print(f"Chosen Action: {action}")

        return action
