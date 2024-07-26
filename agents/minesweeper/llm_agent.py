# File: minesweeper_agent.py
import time
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.provider_type import ProviderType
from agents.base_llm_agent import BaseLLMAgent
from agents.minesweeper.agent_action import MinesweeperAction as AgentAction

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
        {strategy}

        {strategyImprovementNotes}

        Based on the current state and strategy, decide your next action.
        Format your response as: ACTION X Y
        Where ACTION is either REVEAL or FLAG, and X and Y are the 0-indexed coordinates.

        Examples:
        REVEAL 3 4 (reveal the cell at coordinates 3,4)
        FLAG 2 1 (flag the cell at coordinates 2,1)

        Provide only the action in the specified format, without any explanation.
        """
        
        # set size and visited
        self.size = size
        self.visited = set()

        # call the parent constructor
        super().__init__(id, name, description, provider, model_name, prompt_template)

        # update the prompt template to CoT version
        self.prompt_template = prompt_template

        # set the prompt template
        self.prompt = PromptTemplate(input_variables=["state","size","visited","strategy", "strategyImprovementNotes"], template=prompt_template)
        
        # setup the chain with the prompt and llm
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

        # setup self improvement notes
        self.self_improvement_notes = ""

    def get_action(self, step, state: str):
        # get the action history
        visited_str = "\n".join([f"{'FLAG' if flag else 'REVEAL'} {row} {col}" for (row, col, flag) in self.visited])
        
        # start time for measuring decision time
        start_time = time.time()

        # call the chain
        response = self.chain.run(state=state, visited=visited_str, size=self.size, strategy=self.strategy, strategyImprovementNotes=self.self_improvement_notes)
        
        # extract the thought process and final output
        thought_process = self.extract_tag_content(response, "agentThinking")
        final_output = self.extract_tag_content(response, "finalOutput")
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            # get the action
            action = AgentAction.from_string(final_output.strip())

            # check if the action has already been performed
            if (action.row, action.col, action.action_type == AgentAction.ActionType.FLAG) in self.visited:
                return None
            elif 0 <= action.row < self.size and 0 <= action.col < self.size:
                self.visited.add((action.row, action.col, action.action_type == AgentAction.ActionType.FLAG))

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
            else:
                # invalid action
                return None
        except ValueError as e:
            print(f"Invalid action from LLM: {response}. Error: {e}")
            for i in range(self.size):
                for j in range(self.size):
                    if (i, j, False) not in self.visited and (i, j, True) not in self.visited:
                        self.visited.add((i, j, False))

                        # log the state, thought process, and decision
                        thought_process = "Fallback action due to invalid LLM response."
                        time_completed = time.time() - start_time  # Measure the time taken to decide
                        fallback_action = AgentAction(AgentAction.ActionType.REVEAL, i, j)
                        self.logger.log_decision(
                            self.game_id,
                            step,
                            state,
                            thought_process,
                            str(fallback_action),  # Use the string representation of the fallback action for logging
                            str(fallback_action),  # Use the string representation of the fallback action for logging
                            time_completed
                        )
                        
                        return fallback_action
