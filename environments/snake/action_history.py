# File: environments/snake/action_history.py
from agents.snake.snake_action import SnakeAction

class ActionHistory:
    def __init__(self):
        # Initialize the history list
        self.history = []

    def add_record(self, step, snake_head_position, snake_direction, snake_length, action):
        # Ensure snake_direction and action are stored as integers
        if isinstance(snake_direction, SnakeAction):
            snake_direction_value = snake_direction.action
        elif isinstance(snake_direction, str):
            snake_direction_value = SnakeAction.from_string(snake_direction).action
        else:
            snake_direction_value = snake_direction

        # get the record
        record = {
            "step": step,
            "snake_head_position": snake_head_position,
            "snake_direction": snake_direction_value,
            "snake_length": snake_length,
            "action": action
        }

        # add the record to the history
        self.history.append(record)
    
    def get_history(self):
        """Return the full action history."""
        return self.history

    def clear(self):
        """Clear the action history."""
        self.history = []

