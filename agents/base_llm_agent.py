# File: agents/base_llm_agent.py
from abc import ABC, abstractmethod
import time
import dotenv
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI, ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.agent_logging import AgentLogger
from agents.agent_type import AgentType
from agents.provider_type import ProviderType

# load environment variables .env file
dotenv.load_dotenv()

class BaseLLMAgent(ABC):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, prompt_template: str):
        # set the agent details
        self.id = id
        self.name = name
        self.description = description
        self.llm_provider = provider
        self.model_name = model_name

        # Initialize logger with default values
        self.logger = AgentLogger(agent_id=self.id)

        # get the llm
        self.llm = self._get_llm(provider, model_name)

        # set the prompt template
        self.prompt = PromptTemplate(input_variables=["state"], template=prompt_template)
        
        # setup the chain with the prompt and llm
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def _get_llm(self, provider: str, model_name: str):
        # check for openai
        if provider == "openai":
            # Models that typically don't support temperature customization
            # Including o1, o3, o4 series and gpt-5
            no_temp_patterns = ['o1', 'o3', 'o4', 'gpt-5']
            
            # Check if the model matches any of the patterns that don't support temperature
            uses_default_temp = any(model_name.startswith(pattern) for pattern in no_temp_patterns)
            
            if uses_default_temp:
                # Explicitly set temperature to 1.0 (the only supported value)
                print(f"Note: Using temperature=1.0 for {model_name} (only supported value)")
                return ChatOpenAI(model_name=model_name, temperature=1.0)
            else:
                # For other models, try with temperature but fall back if needed
                try:
                    return ChatOpenAI(model_name=model_name, temperature=0.7)
                except Exception as e:
                    error_msg = str(e).lower()
                    if "temperature" in error_msg and ("unsupported" in error_msg or "does not support" in error_msg):
                        print(f"Note: {model_name} doesn't support custom temperature, using 1.0")
                        return ChatOpenAI(model_name=model_name, temperature=1.0)
                    else:
                        # Re-raise if it's a different error
                        raise e
                        
        elif provider == "anthropic":
            # anthropic
            return ChatAnthropic(model=model_name, temperature=0.7)
        elif provider == "ollama":
            # ollama
            return Ollama(model=model_name, temperature=0.7)
        else:
            # unsupported
            raise ValueError(f"Unsupported provider: {provider}")

    @abstractmethod
    def get_action(self, state: str):
        pass

    def reset(self):
        self.visited.clear()

    def extract_tag_content(self, text: str, tag: str) -> str:
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        start_index = text.find(start_tag) + len(start_tag)
        end_index = text.find(end_tag)
        return text[start_index:end_index].strip() if start_index != -1 and end_index != -1 else text
    
    @property
    def agent_type(self) -> AgentType:
        """Return the type of the agent."""
        return AgentType.LLM

    def game_over(self, step:int, state: str):
        # set the time completed
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')

        # log the state, thought process, and decision
        self.logger.log_decision(self.game_id, step, state, "", "", "", time_completed, self.llm_provider, self.model_name)