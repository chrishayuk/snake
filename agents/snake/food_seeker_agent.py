# File: agents/snake/food_seeker_agent.py
from agents.snake.agent_action import AgentAction
from agents.snake.classic_agent import ClassicAgent

class FoodSeekerAgent(ClassicAgent):
    def get_action(self, state) -> AgentAction:
        # Check if the state is a string or numpy array
        if isinstance(state, str):
            state = self.parse_state_string(state)

        # get the position of the snake head
        snake_head = self.get_snake_head_position(state)

        # get the food position
        food = self.get_food_position(state)
        
        # Head towards the food policy
        if food[0] < snake_head[0]:
            return AgentAction.UP
        elif food[0] > snake_head[0]:
            return AgentAction.DOWN
        elif food[1] < snake_head[1]:
            return AgentAction.LEFT
        else:
            return AgentAction.RIGHT