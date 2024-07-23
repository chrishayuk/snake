# File: agents/snake/llm_agent_cot.py
import time
from agents.provider_type import ProviderType
from agents.snake.agent_action import AgentAction
from agents.snake.llm_agent import LLMAgent as BaseLLMAgent

class LLMAgent(BaseLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, size: int):
        prompt_template = """
        You are an AI playing a game of Minesweeper. The game is played on a grid of size {size}x{size}.
        Grid symbols:
        . : unrevealed cell
        F : flagged cell
        1-8 : revealed cell with the number of adjacent mines
        * : revealed mine (game over)
        [space] : revealed cell with no adjacent mines

        Current game state:
        {state}

        Previously taken actions (do not repeat these):
        {visited}

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
        super().__init__(id, name, description, provider, model_name, prompt_template)
    