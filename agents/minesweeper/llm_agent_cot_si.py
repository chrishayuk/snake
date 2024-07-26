# File: agents/snake/llm_agent_cot.py
import time
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.provider_type import ProviderType
from agents.minesweeper.llm_agent import LLMAgent as BaseLLMAgent

class LLMAgent(BaseLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, size: int):
        self.strategy = """
Initial Move: Start with corners or edges, as they have fewer adjacent cells.
Flagging Mines: When a revealed number matches the count of adjacent unrevealed cells, flag those cells as mines.
Revealing Safe Cells: When a revealed number matches the count of adjacent flagged cells, reveal the other adjacent unrevealed cells.
Pattern Recognition: Look for patterns (e.g., two 1s diagonally adjacent often indicate a safe cell between them).
Probability: If unsure, choose the cell with the highest probability of being safe based on surrounding numbers.
Avoid Guessing: Only guess if no other logical moves are available.
Decision-Making Process:

Analyze the current state to identify revealed cells, flagged cells, and unrevealed cells.
Identify cells to flag: For any revealed number that matches the count of adjacent unrevealed cells, flag those cells.
Identify cells to reveal: For any revealed number that matches the count of adjacent flagged cells, reveal the other adjacent unrevealed cells.
Evaluate patterns to find additional safe cells to reveal or flag.
Consider probabilities to decide the safest cell to reveal if no definite safe moves are identified.
Make a decision that aligns with the strategy to minimize risk and progress the game.

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

**The following is strategy improvement notes, this is notes you have made from previous games to improve the strategy.**
        These are the most IMPORTANT NOTES, and should be used to override/improve any strategy thinking.
        These notes are where things have gone wrong in the past with the strategy, and you should use them to improve your decision-making.
        Revise these notes before every decision.

        **Strategy Improvement Notes:**
        {strategyImprovementNotes}

Provide your thinking in the `agentThinking` tags e.g.
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
        self.prompt = PromptTemplate(input_variables=["state","size","visited","strategy","strategyImprovementNotes"], template=prompt_template)
        
        # setup the chain with the prompt and llm
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

        # setup self improvement notes
        self.self_improvement_notes = ""
    
    def game_over(self, step: int, state: str):
        # set the time completed
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')

        # log the state, thought process, and decision
        self.logger.log_decision(self.game_id, step, state, "", "", "", time_completed)

        # create a game summary (this should include key events and outcomes of the game)
        summary = f"Game ended at step {step}. Strategy:\n{self.strategy}\nFinal state:\n{state}\nPrevious Strategy-Improvement Notes:\n{self.self_improvement_notes}"

        # reflect on the game and update self-improvement notes
        self.self_improvement_notes = self.reflect_on_game(self.strategy, summary)

        # log self-improvement notes
        self.logger.log_self_improvement_notes(self.game_id, step, self.self_improvement_notes)
    
    def reflect_on_game(self, strategy, summary):
        reflection_prompt_template = """
You have just completed a game of Snake. Reflect on the game to identify areas for improvement.

Strategy:
{strategy}

Game Summary:
{summary}

Strategy Improvement Notes:

Reflect on your performance and suggest improvements for future games.
This must be in the form of prompts and could include examples of good or bad moves.
These should be additions to the strategy to improve the decision-making.
These will be placed with the strategy for future games, so make them super sharp improvements to the strategy to fix errors in this gameplay.
Place the notes to improve the strategy in the strategyImprovementNotes tags.
You should consider these notes as standalone and additive to complement the existing strategy. The agent won't have access to the previous game history, actions or steps, so pure strategy notes.
Keep existing notes that are useful and improve, do not overwrite, blend and improve.
Be specific, give examples of why a move was wrong, using positions and actions to clarify the improvement.  DO NOT refer to steps as agent won't have access to previous history.  Only give standalone examples with coordinates.
Do not lose notes, but can consolidate previous notes into improved strategy improvement notes.

<strategyImprovementNotes>
place notes here
</strategyImprovementNotes>
"""

        # set the reflection chain
        reflection_prompt = PromptTemplate(input_variables=["summary","strategy"], template=reflection_prompt_template)
        reflection_chain = LLMChain(llm=self.llm, prompt=reflection_prompt)

        # set the reflection chain
        response = reflection_chain.run({"summary": summary, "strategy": strategy})

        # Extract and return the self-improvement notes
        return response.strip()
