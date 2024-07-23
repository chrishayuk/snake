# File: agents/snake/llm_agent.py
import time
from agents.agent_type import AgentType
from agents.provider_type import ProviderType
from agents.base_llm_agent import BaseLLMAgent
from agents.snake.agent_action import AgentAction

class LLMAgent(BaseLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str):
        prompt_template = """
        You are an AI controlling a snake in a classic Snake game. The game is played on a grid.

        Grid symbols:
        H : Head of the snake (current position)
        O : Body of the snake
        F : Food that the snake should eat
        . : Empty square

        Current game state:
        {state}

        Snake game strategy:
        1. Primary goal: Move towards the food (F) to grow the snake.
        2. Avoid collisions: Don't move into walls or the snake's body (O).
        3. Plan ahead: Consider the snake's length when moving towards food.
        4. Use space efficiently: Try to move in a way that leaves open paths.
        5. In tight spaces, follow the snake's tail to survive.
        6. If no clear path to food exists, move to maximize empty space around the head.

        Based on the current state and strategy, decide the snake's next move.
        Choose from: UP, DOWN, LEFT, RIGHT

        Consider these factors in order:
        1. Immediate survival (avoid collisions)
        2. Moving towards food
        3. Long-term survival (maintaining open paths)

        Provide your answer as a single word (UP, DOWN, LEFT, or RIGHT) with no additional explanation.
        """
        super().__init__(id, name, description, provider, model_name, prompt_template)

    def get_action(self, state: str):
        # call the llm
        response = self.chain.run(state=state)

        # map the action
        action_map = {
            "UP": AgentAction.UP,
            "DOWN": AgentAction.DOWN,
            "LEFT": AgentAction.LEFT,
            "RIGHT": AgentAction.RIGHT
        }

        # set the time completed
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # response stripped
        response_stripped = response.strip().upper(),

        # log the state, thought process, and decision
        self.logger.log_decision(self.game_id, state, "", response_stripped, response, time_completed)

        # return the action
        return action_map.get(response_stripped, AgentAction.RIGHT)