# File: agents/treasure_hunt/treasure_hunt_agent.py
from agents.provider_type import ProviderType
from agents.treasure_hunt.base_llm_agent import BaseTreasureHuntLLMAgent
from agents.treasure_hunt.prompt_templates.strategy_prompt_template import common_strategy
from agents.treasure_hunt.prompt_templates.basic_prompt_template import basic_prompt_template

class LLMAgent(BaseTreasureHuntLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, size: int):
        # set the strategy
        strategy = common_strategy

        # set the prompt template
        prompt_template = basic_prompt_template

        # self improvement notes
        self.self_improvement_notes = ""
        
        # call the constructor
        super().__init__(id, name, description, provider, model_name, size, prompt_template, strategy)

