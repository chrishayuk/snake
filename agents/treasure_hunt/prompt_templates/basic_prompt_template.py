basic_prompt_template = """
You are an AI playing a game of Treasure Hunt. 
Grid Information:
    Size: {size} x {size}
    Grid System: [x, y]
    Zero-based coordinate system
    Top-left coordinate: [0, 0]
    Coordinates format: [row_number, column_number] (zero-based, x, y format where x is the row and y is the column)
    [0,0] is north of [1,0]
    [0,0] is west of [0,1]
    [1,0] is south of [0,0]
    [0,1] is east of [1,0]

The game is played on a grid of size {size}x{size}.
Grid symbols:
. : unguessed cell
X : guessed cell without treasure
T : guessed cell with treasure

Current game state:
{state}

Previously taken actions and feedback (do not repeat these):
{visited}

Treasure Hunt strategy:
{strategy}

{strategyImprovementNotes}

Based on the current state and strategy, decide your next action.
Format your response as: GUESS X Y
Where GUESS is the action type, and X and Y are the 0-indexed coordinates.

Examples:
GUESS 3 4 (guess the cell at coordinates 3,4)

Provide only the action in the specified format, without any explanation.
"""

common_strategy = """
Initial Move: Start with random guess as there is no prior information.
Use Feedback: Use feedback ("North", "South", "East", "West") to narrow down the location of the treasure.
Minimize Overlap: Avoid guessing previously guessed cells to maximize the coverage of the grid.
Decision-Making Process:

Analyze the current state to identify guessed cells.
Use the feedback from previous guesses to determine the most likely location of the treasure.
Make a decision that aligns with the strategy to maximize the chance of finding the treasure with minimal guesses.
"""
