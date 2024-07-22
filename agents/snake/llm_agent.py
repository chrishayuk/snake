# File: llm_agent.py
import dotenv
from typing import Literal
from agents.snake.agent_action import AgentAction
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# load environment variables .env file
dotenv.load_dotenv()

class LLMAgent:
    def __init__(self, provider: Literal["openai", "ollama"], model_name: str):
        # get the llm
        self.llm = self._get_llm(provider, model_name)

        # setup the prompt
        self.prompt = PromptTemplate(
            input_variables=["state"],
            template="""
            You are an AI controlling a snake in a classic Snake game. The game is played on a grid.

            Grid symbols:
            H : Head of the snake (current position)
            O : Body of the snake
            F : Food that the snake should eat
            . : Empty square

            Current game state:
            {state}

            Snake game strategy:
            1. Primary goal: Move towards the food (F) to grow the snake.
            2. Avoid collisions: Don't move into walls or the snake's body (O).
            3. Plan ahead: Consider the snake's length when moving towards food.
            4. Use space efficiently: Try to move in a way that leaves open paths.
            5. In tight spaces, follow the snake's tail to survive.
            6. If no clear path to food exists, move to maximize empty space around the head.

            Based on the current state and strategy, decide the snake's next move.
            Choose from: UP, DOWN, LEFT, RIGHT

            Consider these factors in order:
            1. Immediate survival (avoid collisions)
            2. Moving towards food
            3. Long-term survival (maintaining open paths)

            Provide your answer as a single word (UP, DOWN, LEFT, or RIGHT) with no additional explanation.
            """
        )

        # set up the chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    @property
    def name(self) -> str:
        """Return the name of the agent."""
        return "LLM Agent"

    @property
    def agent_type(self) -> str:
        """Return the type of the agent."""
        return "Snake Agent"
    
    def _get_llm(self, provider: str, model_name: str):
        if provider == "openai":
            # openai
            return ChatOpenAI(model_name=model_name)
        elif provider == "anthropic":
            # ollama
            return ChatAnthropic(model=model_name)
        elif provider == "ollama":
            # ollama
            return Ollama(model=model_name)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_action(self, state: str) -> AgentAction: 
        # execute the llm       
        response = self.chain.run(state=state)
        
        # let's map the response
        action_map = {
            "UP": AgentAction.UP,
            "DOWN": AgentAction.DOWN,
            "LEFT": AgentAction.LEFT,
            "RIGHT": AgentAction.RIGHT
        }
        
        # Default to RIGHT if invalid response
        return action_map.get(response.strip().upper(), AgentAction.RIGHT)