# File: agents/snake/base_llm_snake_agent.py

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.base_llm_agent import BaseLLMAgent
from agents.provider_type import ProviderType
from agents.snake.snake_action import SnakeAction
from agents.agent_tag_utils import extract_final_output, extract_thought_process, extract_time_completed
from agents.snake.prompt_templates.strategy_prompt_template import common_strategy
from agents.snake.prompt_templates.reflection_prompt_template import reflection_prompt_template
import time

class BaseSnakeLLMAgent(BaseLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, prompt_template: str):
        # Call the parent constructor
        super().__init__(id, name, description, provider, model_name, prompt_template)
        self.strategy = common_strategy
        self.self_improvement_notes = ""

        # Update the prompt to include strategy and self-improvement notes
        self.prompt = PromptTemplate(input_variables=["state", "strategy"], template=prompt_template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def get_action(self, step: int, state: str):
        # get the response
        response = self.chain.run(state=state, strategy=self.strategy)

        # extract the tags
        thought_process = extract_thought_process(response)
        final_output = extract_final_output(response)
        time_completed = extract_time_completed(response)
        
        # log the decision
        self.logger.log_decision(self.game_id, step, state, thought_process, final_output, response, time_completed, self.llm_provider, self.model_name)

        # get the mapping
        action_map = {
            "UP": SnakeAction.UP,
            "DOWN": SnakeAction.DOWN,
            "LEFT": SnakeAction.LEFT,
            "RIGHT": SnakeAction.RIGHT
        }

        # clean the output
        final_output_cleaned = final_output.strip().upper()

        # get mapping
        action = action_map.get(final_output_cleaned, SnakeAction.RIGHT)

        # return the action
        return action

    def game_over(self, step: int, state: str):
        # call the base
        super().game_over(step, state)