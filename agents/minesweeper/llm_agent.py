# File: minesweeper_agent.py
from agents.provider_type import ProviderType
from agents.base_llm_agent import BaseLLMAgent
from agents.minesweeper.agent_action import MinesweeperAction as AgentAction
class LLMAgent(BaseLLMAgent):
    def __init__(self, provider: ProviderType, model_name: str, size: int):
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
        1. Always start with corners or edges, as they have fewer adjacent cells.
        2. When a revealed number matches the count of adjacent unrevealed cells, all those cells are mines and should be flagged.
        3. When a revealed number matches the count of adjacent flagged cells, all other adjacent unrevealed cells are safe to reveal.
        4. Look for patterns: two 1s diagonally adjacent often indicate a safe cell between them.
        5. If unsure, choose the cell with the highest probability of being safe based on surrounding numbers.
        6. Avoid guessing unless absolutely necessary.

        Based on the current state and strategy, decide your next action.
        Format your response as: ACTION X Y
        Where ACTION is either REVEAL or FLAG, and X and Y are the 0-indexed coordinates.

        Examples:
        REVEAL 3 4 (reveal the cell at coordinates 3,4)
        FLAG 2 1 (flag the cell at coordinates 2,1)

        Provide only the action in the specified format, without any explanation.
        """
        super().__init__(provider, model_name, prompt_template, size)

    def get_action(self, state: str):
        # get the action history
        visited_str = "\n".join([f"{'FLAG' if flag else 'REVEAL'} {row} {col}" for (row, col, flag) in self.visited])
        
        # call the chain
        response = self.chain.run(state=state, visited=visited_str, size=self.size)

        try:
            # get the action
            action = AgentAction.from_string(response.strip())

            # check if the action has already been performed
            if (action.row, action.col, action.action_type == AgentAction.ActionType.FLAG) in self.visited:
                print(f"Action {action} has already been visited.")
                return None
            elif 0 <= action.row < self.size and 0 <= action.col < self.size:
                self.visited.add((action.row, action.col, action.action_type == AgentAction.ActionType.FLAG))
                return action
            else:
                # invalid action
                print(f"Invalid action out of bounds: {action}.")
                return None
        except ValueError as e:
            print(f"Invalid action from LLM: {response}. Error: {e}")
            for i in range(self.size):
                for j in range(self.size):
                    if (i, j, False) not in self.visited and (i, j, True) not in self.visited:
                        self.visited.add((i, j, False))
                        return AgentAction(AgentAction.ActionType.REVEAL, i, j)
