# File: agents/snake/llm_agent_enhanced.py
import time
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.provider_type import ProviderType
from agents.snake.agent_action import AgentAction
from agents.snake.llm_agent import LLMAgent as BaseLLMAgent

class LLMAgent(BaseLLMAgent):
    def __init__(self, id, name: str, description: str, provider: ProviderType, model_name: str):
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

        prompt_template = """
        You are an AI controlling a snake in a classic Snake game. The game is played on a rectangular grid.

        **Grid Information:**

        Size: 10 x 10
        Grid System: [x, y]
        Zero-based coordinate system
        Top-left coordinate: [0, 0]
        Bottom-right coordinate: [9, 9]
        Coordinates format: [column_number, row_number] (zero-based, x, y format where x is the column and y is the row)
        Moving UP decreases Y by 1.
        Moving DOWN increases Y by 1.
        Moving LEFT decreases X by 1.
        Moving RIGHT increases X by 1.

        **Grid Symbols:**

        H: Head of the snake (current position)
        O: Body of the snake
        F: Food that the snake should eat
        .: Empty square

        **Current Game State:**
        {state}

        **Snake Game Strategy:**
        {strategy}

        **The following is strategy improvement notes, this is notes you have made from previous games to improve the strategy.**
        These are the most IMPORTANT NOTES, and should be used to override/improve any strategy thinking.
        These notes are where things have gone wrong in the past with the strategy, and you should use them to improve your decision-making.
        Revise these notes before every decision.

        **Strategy Improvement Notes:**
        {strategyImprovementNotes}

        And REMEMEBER you are a hungry snake and your primary goal is to eat FOOD.
        
        Provide your thinking in the `agentThinking` tags e.g.

        <agentThinking>
        **Explain your thought process, considering:**
        1. **Current position of the snake's head** (in [column, row] format)
        2. **Location of the food** (in [column, row] format)
        3. **Safe moves available** (list all safe moves with coordinates they lead to)
        4. **Potential future moves and their consequences** (evaluate each move with coordinates they lead to)
        5. **How your chosen move aligns with the game strategy** (justify your choice, especially how it brings the snake closer to the food to achieve a high score)
        </agentThinking>

        Provide your final decision in a `finalOutput` tag with a single word: UP, DOWN, LEFT, or RIGHT. e.g.,
        <finalOutput>
        final decision goes here
        </finalOutput>
        """

        # call the parent constructor with the CoT prompt template
        super().__init__(id, name, description, provider, model_name)
        
        # update the prompt template to CoT version
        self.prompt_template = prompt_template

        # set the prompt template
        self.prompt = PromptTemplate(input_variables=["state", "strategy", "strategyImprovementNotes"], template=prompt_template)
        
        # setup the chain with the prompt and llm
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

        # setup self improvement notes
        self.self_improvement_notes = ""
    
    def get_action(self, step:int, state: str):
        # call the llm
        response = self.chain.run(state=state, strategy=self.strategy, strategyImprovementNotes=self.self_improvement_notes)

        # extract the thought process and final output
        thought_process = self.extract_tag_content(response, "agentThinking")
        final_output = self.extract_tag_content(response, "finalOutput")
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')

        # log the state, thought process, and decision
        self.logger.log_decision(self.game_id, step, state, thought_process, final_output, response, time_completed)

        # map the action
        action_map = {
            "UP": AgentAction.UP,
            "DOWN": AgentAction.DOWN,
            "LEFT": AgentAction.LEFT,
            "RIGHT": AgentAction.RIGHT
        }

        # return the action
        return action_map.get(final_output.strip().upper(), AgentAction.RIGHT)

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
    