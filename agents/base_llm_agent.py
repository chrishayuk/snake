# File: base_llm_agent.py
from abc import ABC, abstractmethod
import dotenv
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI, ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.agent_logging import Logger
from agents.provider_type import ProviderType

# load environment variables .env file
dotenv.load_dotenv()

class BaseLLMAgent(ABC):
    def __init__(self, provider: ProviderType, model_name: str, prompt_template: str, size: int = None):
        # set size and visited
        self.size = size
        self.visited = set()

        # Initialize logger with default values
        self.logger = Logger(game_id="default_game", agent_id="default_agent")

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
