# File: llm_agent.py
import dotenv
from typing import Literal
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from agent_action import MinesweeperAction as AgentAction

# load environment variables .env file
dotenv.load_dotenv()

class LLMAgent:
    def __init__(self, provider: Literal["openai", "ollama", "anthropic"], model_name: str):
        # get the llm
        self.llm = self._get_llm(provider, model_name)

        # setup the prompt
        self.prompt = PromptTemplate(
            input_variables=["state"],
            template="""
            You are an AI playing a game of Minesweeper. The game is played on a grid.
            Grid symbols:
            . : unrevealed cell
            F : flagged cell
            1-8 : revealed cell with the number of adjacent mines
            * : revealed mine (game over)
            [space] : revealed cell with no adjacent mines

            Current game state:
            {state}

            Minesweeper strategy:
            1. Always start with corners or edges, as they have fewer adjacent cells.
            2. When a revealed number matches the count of adjacent unrevealed cells, all those cells are mines and should be flagged.
            3. When a revealed number matches the count of adjacent flagged cells, all other adjacent unrevealed cells are safe to reveal.
            4. Look for patterns: two 1s diagonally adjacent often indicate a safe cell between them.
            5. If unsure, choose the cell with the highest probability of being safe based on surrounding numbers.
            6. Avoid guessing unless absolutely necessary.

            Based on the current state and strategy, decide your next action.
            Format your response as: ACTION X Y
            Where ACTION is either REVEAL or FLAG, and X and Y are the 0-indexed coordinates.

            Examples:
            REVEAL 3 4 (reveal the cell at coordinates 3,4)
            FLAG 2 1 (flag the cell at coordinates 2,1)

            Provide only the action in the specified format, without any explanation.
            """
        )

        # set up the chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def _get_llm(self, provider: str, model_name: str):
        if provider == "openai":
            return ChatOpenAI(model_name=model_name)
        elif provider == "anthropic":
            return ChatAnthropic(model=model_name)
        elif provider == "ollama":
            return Ollama(model=model_name)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_action(self, state):
        # Use the LLM to generate an action based on the state
        response = self.chain.run(state=state)
        
        # Parse the LLM's response into a MinesweeperAction
        try:
            action = AgentAction.from_string(response.strip())
            return action
        except ValueError as e:
            print(f"Invalid action from LLM: {response}. Error: {e}")
            # If the LLM's response is invalid, return a default action
            return AgentAction(AgentAction.ActionType.REVEAL, 0, 0)