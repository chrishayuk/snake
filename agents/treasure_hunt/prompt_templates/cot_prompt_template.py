cot_template = """
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

Decision-Making Process:
1. Analyze the current state to identify guessed cells.
2. Use the feedback from previous guesses to determine the most likely location of the treasure.
3. Make a decision that aligns with the strategy to maximize the chance of finding the treasure with minimal guesses.
4. Avoid repeating guesses to maximize coverage.

Provide your thinking in the agentThinking tags e.g.
<agentThinking>
**Explain your thought process, considering:**
1. **Current guessed cells** and their feedback.
2. **Potential next guess** based on the feedback and current state.
3. **Why the chosen guess** aligns with the strategy to find the treasure efficiently.
</agentThinking>

Provide your final decision in a <finalOutput> tag in the format: GUESS X Y. e.g.,
<finalOutput>
GUESS 3 4
</finalOutput>
"""