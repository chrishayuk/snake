# File: agents/treasure_hunt/llm_agent_cot.py
import time
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.provider_type import ProviderType
from agents.base_llm_agent import BaseLLMAgent
from agents.treasure_hunt.treasure_hunt_action import TreasureHuntAction


class LLMAgent(BaseLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str, size: int):
        self.strategy = """
Initial Move: Start with a random guess as there is no prior information.
Use Feedback: Use feedback ("North", "South", "East", "West") to narrow down the location of the treasure.
Minimize Overlap: Avoid guessing previously guessed cells to maximize the coverage of the grid.
Decision-Making Process:
Analyze the current state to identify guessed cells.
Use the feedback from previous guesses to determine the most likely location of the treasure.
Make a decision that aligns with the strategy to maximize the chance of finding the treasure with minimal guesses.
"""

        prompt_template = """
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
        # set size and visited
        self.size = size
        self.visited = set()

        # call the parent constructor
        super().__init__(id, name, description, provider, model_name, prompt_template)

        # update the prompt template to CoT version
        self.prompt_template = prompt_template

        # set the prompt template
        self.prompt = PromptTemplate(input_variables=["state", "size", "visited", "strategy"], template=prompt_template)

        # setup the chain with the prompt and llm
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

        # setup self improvement notes
        self.self_improvement_notes = ""

    def get_action(self, step, state: str):
        # get the action history
        visited_str = "\n".join([f"GUESS {row} {col}: {feedback}" for (row, col, feedback) in self.visited])

        # start time for measuring decision time
        start_time = time.time()

        # call the chain
        response = self.chain.run(state=state, visited=visited_str, size=self.size, strategy=self.strategy)

        # extract the thought process and final output
        thought_process = self.extract_tag_content(response, "agentThinking")
        final_output = self.extract_tag_content(response, "finalOutput")
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            # get the action
            action = TreasureHuntAction.from_string(final_output.strip())

            # validate the action coordinates
            if not (0 <= action.row < self.size and 0 <= action.col < self.size):
                raise ValueError("Invalid action coordinates")

            # check if the action has already been performed
            if any(action.row == r and action.col == c for r, c, _ in self.visited):
                return None
            else:
                self.visited.add((action.row, action.col, "Feedback will be provided"))

                # log decision
                self.logger.log_decision(
                    self.game_id,
                    step,
                    state,
                    thought_process,
                    str(action),  # Use the string representation of the action for logging
                    response,
                    time_completed
                )

                return action
        except ValueError as e:
            print(f"Invalid action from LLM: {response}. Error: {e}")
            for i in range(self.size):
                for j in range(self.size):
                    if not any(i == r and j == c for r, c, _ in self.visited):
                        self.visited.add((i, j, "Fallback action"))

    def extract_tag_content(self, text, tag):
        """Extract content between specified tags."""
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        start_index = text.find(start_tag) + len(start_tag)
        end_index = text.find(end_tag)
        if start_index == -1 or end_index == -1:
            return ""
        return text[start_index:end_index].strip()
