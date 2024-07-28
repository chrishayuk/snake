# llm_agent.py

from agents.provider_type import ProviderType
from agents.snake.base_llm_snake_agent import BaseSnakeLLMAgent
from agents.snake.prompt_templates.basic_prompt_template import basic_prompt_template

class LLMAgent(BaseSnakeLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str):
        super().__init__(id, name, description, provider, model_name, basic_prompt_template)
