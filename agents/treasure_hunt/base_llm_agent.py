# File: agents/treasure_hunt/llm_agent_base.py
import time
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.agent_tag_utils import extract_final_output, extract_thought_process, extract_time_completed
from agents.provider_type import ProviderType
from agents.base_llm_agent import BaseLLMAgent
from agents.treasure_hunt.treasure_hunt_action import TreasureHuntAction

class BaseTreasureHuntLLMAgent(BaseLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, size: int, prompt_template: str, strategy: str):
        # set the strategy and size
        self.strategy = strategy
        self.size = size
        self.visited = set()

        # call the parent constructor
        super().__init__(id, name, description, provider, model_name, prompt_template)

        # set the prompt template
        self.prompt_template = prompt_template
        self.prompt = PromptTemplate(input_variables=["state", "size", "visited", "strategy", "strategyImprovementNotes"], template=prompt_template)

        # setup the chain with the prompt and llm
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

        # setup self improvement notes
        self.self_improvement_notes = ""

    def get_action(self, step, state: str):
        # get the action history
        visited_str = "\n".join([f"GUESS {row} {col}: {feedback}" for (row, col, feedback) in self.visited])

        # start time for measuring decision time
        start_time = time.time()

        # call the chain
        response = self.chain.run(state=state, visited=visited_str, size=self.size, strategy=self.strategy, strategyImprovementNotes=self.self_improvement_notes)

        # extract the thought process and final output
        thought_process = extract_thought_process(response)
        final_output = extract_final_output(response)
        time_completed = extract_time_completed(response)

        try:
            # get the action
            action = TreasureHuntAction.from_string(final_output.strip())

            # validate the action coordinates
            if not (0 <= action.row < self.size and 0 <= action.col < self.size):
                raise ValueError("Invalid action coordinates")

            # check if the action has already been performed
            if any(action.row == r and action.col == c for r, c, _ in self.visited):
                return None
            else:
                self.visited.add((action.row, action.col, "Feedback will be provided"))

                # log decision
                self.logger.log_decision(
                    self.game_id,
                    step,
                    state,
                    thought_process,
                    str(action),  # Use the string representation of the action for logging
                    response,
                    time_completed
                )

                return action
        except ValueError as e:
            print(f"Invalid action from LLM: {response}. Error: {e}")
            for i in range(self.size):
                for j in range(self.size):
                    if not any(i == r and j == c for r, c, _ in self.visited):
                        self.visited.add((i, j, "Fallback action"))

    def extract_tag_content(self, text, tag):
        """Extract content between specified tags."""
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        start_index = text.find(start_tag) + len(start_tag)
        end_index = text.find(end_tag)
        if start_index == -1 or end_index == -1:
            return ""
        return text[start_index:end_index].strip()
