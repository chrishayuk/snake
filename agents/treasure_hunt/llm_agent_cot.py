# File: agents/treasure_hunt/llm_agent_cot.py
from agents.provider_type import ProviderType
from agents.treasure_hunt.base_llm_agent import BaseTreasureHuntLLMAgent
from agents.treasure_hunt.prompt_templates.strategy_prompt_template import common_strategy
from agents.treasure_hunt.prompt_templates.cot_prompt_template import cot_template

class LLMAgent(BaseTreasureHuntLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, size: int):
        # set the strategy
        strategy = common_strategy

        # set the prompt template
        prompt_template = cot_template

        # call the parent constructor
        super().__init__(id, name, description, provider, model_name, size, prompt_template, strategy)
