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
            # openai
            return ChatOpenAI(model_name=model_name)
        elif provider == "anthropic":
            # anthropic
            return ChatAnthropic(model=model_name)
        elif provider == "ollama":
            # ollama
            return Ollama(model=model_name)
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
        self.logger.log_decision(self.game_id, step, state, "", "", "", time_completed)
