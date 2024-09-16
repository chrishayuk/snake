# llm_agent_enhanced_si.py
import time
from agents.agent_tag_utils import extract_final_output, extract_thought_process, extract_time_completed
from agents.provider_type import ProviderType
from agents.snake.base_llm_agent import BaseSnakeLLMAgent
from agents.snake.prompt_templates.reflection_prompt_template import reflection_prompt_template
from agents.snake.snake_action import SnakeAction
from agents.snake.prompt_templates.cot_si_prompt_template import cot_si_prompt_template
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class LLMAgent(BaseSnakeLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str):
        super().__init__(id, name, description, provider, model_name, cot_si_prompt_template)
        self.self_improvement_notes = ""

        self.prompt = PromptTemplate(input_variables=["state", "strategy", "strategyImprovementNotes"], template=cot_si_prompt_template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def get_action(self, step:int, state: str):
        # get the response
        response = self.chain.run(state=state, strategy=self.strategy, strategyImprovementNotes=self.self_improvement_notes)

        # extract the thought process and final output
        thought_process = extract_thought_process(response)
        final_output = extract_final_output(response)
        time_completed = extract_time_completed(response)

        # log the decision
        self.logger.log_decision(self.game_id, step, state, thought_process, final_output, response, time_completed, self.llm_provider, self.model_name)

        # get the map
        action_map = {
            "UP": SnakeAction.UP,
            "DOWN": SnakeAction.DOWN,
            "LEFT": SnakeAction.LEFT,
            "RIGHT": SnakeAction.RIGHT
        }

        # return the mapping
        return action_map.get(final_output.strip().upper(), SnakeAction.RIGHT)

    def game_over(self, step: int, state: str):
        # call game over
        super().game_over(step, state)

        # set the summary
        summary = f"Game ended at step {step}. Strategy:\n{self.strategy}\nFinal state:\n{state}\nPrevious Strategy-Improvement Notes:\n{self.self_improvement_notes}"

        # set the self improvement notes
        self.self_improvement_notes = self.reflect_on_game(self.strategy, summary)

         # log self-improvement notes
        self.logger.log_self_improvement_notes(self.game_id, step, self.self_improvement_notes)

    def reflect_on_game(self, strategy, summary):
        # set the reflection prompt
        reflection_prompt = PromptTemplate(input_variables=["summary", "strategy"], template=reflection_prompt_template)

        # call the llm
        reflection_chain = LLMChain(llm=self.llm, prompt=reflection_prompt)
        response = reflection_chain.run({"summary": summary, "strategy": strategy})

        # set the notes
        return self.extract_tag_content(response, "strategyImprovementNotes")