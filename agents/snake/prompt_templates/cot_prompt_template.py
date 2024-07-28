cot_prompt_template = """
You are an AI controlling a snake in a classic Snake game. The game is played on a rectangular grid.

Grid Information:
Size: 10 x 10
Zero-based coordinate system
Top-left coordinate: [0, 0]
Bottom-right coordinate: [9, 9]
Coordinates format: [row_number, column_number]
Moving UP decreases column_number by 1.
Moving DOWN increases column_number by 1.
Moving LEFT decreases row_number by 1.
Moving RIGHT increases row_number by 1.
Grid Symbols:
H: Head of the snake (current position)
O: Body of the snake
F: Food that the snake should eat
.: Empty square
Current Game State:
{state}

Snake Game Strategy:
Primary Goal: Move towards the food (F) to grow the snake.
Avoid Collisions: Ensure the snake does not move into walls or its own body (O).
Plan Ahead: Consider the snake's length and future positions when moving towards food.
Use Space Efficiently: Move in a way that maximizes open paths and avoids tight spaces.
Follow the Tail: In tight spaces, follow the snake's tail to maximize survival.
Maximize Empty Space: If no clear path to food exists, move to maximize empty space around the head.
Decision-Making Process:
Immediate Survival:

Check if the next move will lead to a collision with the wall or the snake's body.
Colliding with the wall will kill the snake and end the game.
Prioritize moves that avoid immediate danger.
Moving Towards Food:

Calculate the Manhattan distance to the food for all valid moves.
Prefer moves that reduce the distance to the food.
Long-term Survival:

Evaluate the available space around the snake's head after each potential move.
Choose moves that leave the snake with more open paths to navigate.
Avoiding Backtracking:

Avoid moves that would reverse the snake's direction unless there is no other safe option.
Steps to Improve:

Check for all valid moves (UP, DOWN, LEFT, RIGHT):
A move is valid if it does not lead to a collision with the wall or the snake's body.
If only one move is valid, choose that move:
This ensures immediate survival.
If multiple moves are valid, prioritize by:
Manhattan distance to food: Moves that reduce the distance to the food.
Open space evaluation: Moves that leave more open paths for future navigation.
Avoid backtracking: Avoid reversing direction unless it's the only safe option.

Provide your thinking in the agentThinking tags e.g.

<agentThinking>
**Explain your thought process, considering:**
1. **Current position of the snake's head** (in [column, row] format)
2. **Location of the food** (in [column, row] format)
3. **Safe moves available** (list all safe moves with coordinates they lead to)
4. **Potential future moves and their consequences** (evaluate each move with coordinates they lead to)
5. **How your chosen move aligns with the game strategy** (justify your choice, especially how it brings the snake closer to the food to achieve a high score)
</agentThinking>

Provide your final decision in a <finalOutput> tag with a single word: UP, DOWN, LEFT, or RIGHT. e.g.,
<finalOutput>
final decision goes here
</finalOutput>
"""