# File: agents/snake/food_seeker_agent.py
import time
from agents.snake.snake_action import SnakeAction
from agents.snake.classic_agent import ClassicAgent

class FoodSeekerAgent(ClassicAgent):
    def get_action(self, step:int, state) -> SnakeAction:
        # Check if the state is a string or numpy array
        if isinstance(state, str):
            state = self.parse_state_string(state)

        # get the position of the snake head
        snake_head = self.get_snake_head_position(state)

        # get the food position
        food = self.get_food_position(state)

        # set the time completed
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Head towards the food policy
        if food[0] < snake_head[0]:
            best_move = SnakeAction.UP
        elif food[0] > snake_head[0]:
            best_move = SnakeAction.DOWN
        elif food[1] < snake_head[1]:
            best_move = SnakeAction.LEFT
        else:
            best_move = SnakeAction.RIGHT
        
        # log the state, thought process, and decision
        self.logger.log_decision(self.game_id, step, state, "", best_move, best_move, time_completed)

        # return the best move
        return best_move
