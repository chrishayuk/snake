# File: agents/snake/llm_agent_cot.py
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.provider_type import ProviderType
from agents.minesweeper.llm_agent import LLMAgent as BaseLLMAgent

class LLMAgent(BaseLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, size: int):
        self.strategy = """
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

        # set the prompt template for CoT agent
        prompt_template = """
        You are an AI playing a game of Minesweeper. The game is played on a grid of size {size}x{size}.

Game Rules and Objectives:

The grid contains hidden mines.
Revealing a cell that contains a mine ends the game.
Revealing a cell that does not contain a mine shows the number of adjacent cells that contain mines (0-8).
The objective is to reveal all cells that do not contain mines and flag all cells that do contain mines.
Grid Information:

Size: {size}x{size}
Top-left coordinate: [0, 0]
Coordinates format: [column_number, row_number] (zero-based, x, y format where x is the column and y is the row)
Grid Symbols:

. : unrevealed cell
F : flagged cell
1-8 : revealed cell with the number of adjacent mines
: revealed mine (game over)
[space] : revealed cell with no adjacent mines
Current Game State:
{state}

Previously Taken Actions:
{visited}

Minesweeper Strategy (in order of priority):

{strategy}

{strategyImprovementNotes}

Make a decision that aligns with the strategy to minimize risk and progress the game.
<agentThinking>
Explain your thought process, considering:
1. **Current position and state of cells** (describe the grid and notable cells)
2. **Potential moves** (list potential cells to flag or reveal)
3. **Evaluation of moves** (analyze the safety and impact of each potential move)
4. **Chosen move** (decide on the move and justify how it aligns with the strategy)
</agentThinking>
Provide your final decision in the format: 
<finalOutput>
ACTION X Y (e.g., REVEAL 3 4 or FLAG 2 1)
</finalOutput>

Example Analysis:

State:

Grid:
1 . . 
1 2 .
. . .
Previously Taken Actions: [REVEAL 0 0, REVEAL 1 0]
<agentThinking>
1. **Current position and state of cells**:
   - The cell at (0, 0) is revealed with a 1.
   - The cell at (1, 0) is revealed with a 1.
   - The cell at (1, 1) is revealed with a 2.
   - Remaining cells are unrevealed.
Potential moves:

FLAG 0 1
REVEAL 1 2
REVEAL 2 0
REVEAL 2 1
REVEAL 2 2
Evaluation of moves:

FLAG 0 1: The cell (0, 1) is likely a mine based on the revealed 1s.
REVEAL 1 2: Revealing (1, 2) is risky without further analysis.
REVEAL 2 0: Revealing (2, 0) could be safe based on surrounding numbers.
REVEAL 2 1: Similar analysis as (2, 0).
REVEAL 2 2: Similar analysis as (2, 0).
Chosen move:

FLAG 0 1: This move aligns with the strategy of flagging likely mines based on surrounding numbers.
</agentThinking>
<finalOutput>
FLAG 0 1
</finalOutput>

Now analyze the current game state provided above and make a decision based on the same process.
        """

        # call the parent constructor with the CoT prompt template
        super().__init__(id, name, description, provider, model_name, size)
        
        # update the prompt template to CoT version
        self.prompt_template = prompt_template

        # set the prompt template
        self.prompt = PromptTemplate(input_variables=["state","size","visited"], template=prompt_template)
        
        # setup the chain with the prompt and llm
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

        # no self improvement notes
        self.self_improvement_notes = ""
