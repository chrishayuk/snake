common_strategy = """
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
"""
