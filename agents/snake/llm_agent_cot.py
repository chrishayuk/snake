# File: agents/snake/llm_agent_enhanced.py
import time
from agents.provider_type import ProviderType
from agents.snake.llm_agent import LLMAgent as BaseLLMAgent

class LLMAgent(BaseLLMAgent):
    def __init__(self, id, name: str, description: str, provider: ProviderType, model_name: str):
        prompt_template = """
You are an AI controlling a snake in a classic Snake game. The game is played on a rectangular grid.

Game Rules and Objectives:

The snake starts with a length of 1 (just the head).
The snake grows by 1 unit each time it eats food.
The game ends if the snake collides with the wall or its own body.
The primary objective is to achieve a high score by eating as much food as possible to grow the snake to the maximum length.
Grid Information:

Size: 10 x 10
Top-left coordinate: [0, 0]
Bottom-right coordinate: [9, 9]
Coordinates format: [column_number, row_number] (zero-based, x, y format where x is the column and y is the row)
Moving UP decreases the row number by 1.
Moving DOWN increases the row number by 1.
Moving LEFT decreases the column number by 1.
Moving RIGHT increases the column number by 1.
Grid Symbols:

H: Head of the snake (current position)
O: Body of the snake
F: Food that the snake should eat
.: Empty square
Current Game State:
{state}

Snake Game Strategy (in order of priority):

Food Acquisition: Move towards the food to grow the snake and achieve a high score.
Survival: Avoid immediate collisions with walls or the snake's body.
Path Planning: Consider the snake's length and maintain open paths.
Space Utilization: Move in a way that maximizes empty space around the head.
Tail Following: In tight spaces, follow the snake's tail to survive.
Decision-Making Process:

Analyze the current state to identify the snake's head, body, and food location.
Determine safe moves that avoid immediate collisions.
Among safe moves, prioritize those that bring the snake closer to the food.
Evaluate long-term consequences of each move (e.g., getting trapped).
Choose the move that best balances immediate goals with long-term survival.
Your task is to decide the snake's next move: UP, DOWN, LEFT, or RIGHT.

<agentThinking>
Explain your thought process, considering:
1. **Current position of the snake's head** (in [column, row] format)
2. **Location of the food** (in [column, row] format)
3. **Safe moves available** (list all safe moves with coordinates they lead to)
4. **Potential future moves and their consequences** (evaluate each move with coordinates they lead to)
5. **How your chosen move aligns with the game strategy** (justify your choice, especially how it brings the snake closer to the food to achieve a high score)
</agentThinking>
Provide your final decision in a <finalOutput> tag with a single word: UP, DOWN, LEFT, or RIGHT. e.g.,
<finalOutput>
UP
</finalOutput>

Example Analysis:

State:

Snake's head: (6, 6) [column, row]
Food: (6, 8) [column, row]
Safe Moves:

UP: From (6, 6) to (6, 5) - This move is safe but does not move towards the food.
DOWN: From (6, 6) to (6, 7) - This move is safe and brings the snake closer to the food.
LEFT: From (6, 6) to (5, 6) - This move is safe but does not move towards the food.
RIGHT: From (6, 6) to (7, 6) - This move is safe but does not move towards the food.
Evaluating Moves:

UP: Moves to (6, 5), does not bring the snake closer to the food.
DOWN: Moves to (6, 7), brings the snake one step closer to the food.
LEFT: Moves to (5, 6), does not bring the snake closer to the food.
RIGHT: Moves to (7, 6), does not bring the snake closer to the food.
Conclusion:

The best move is DOWN to (6, 7), as it brings the snake one step closer to the food, which is the primary goal to achieve a high score.
Final Decision:
<finalOutput>
DOWN
</finalOutput>
Now analyze the current game state provided above and make a decision based on the same process.
"""
        super().__init__(id, name, description, provider, model_name)
    