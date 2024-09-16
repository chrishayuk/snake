# File: agents/tic_tac_toe/llm_agent.py
from agents.provider_type import ProviderType
from agents.tic_tac_toe.base_tic_tac_toe_llm_agent import BaseTicTacToeLLMAgent
from agents.tic_tac_toe.prompt_templates.basic_prompt_template import basic_prompt_template

class LLMAgent(BaseTicTacToeLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str):
        super().__init__(id, name, description, provider, model_name, basic_prompt_template)
