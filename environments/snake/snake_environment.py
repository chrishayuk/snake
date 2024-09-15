# File: environments/snake/snake_environment.py
import numpy as np
import os
import random
import uuid
from agents.snake.snake_action import SnakeAction
from environments.environment_base import Environment
from environments.snake.action_history import ActionHistory
from environments.snake.reward_functions import simple_reward as reward_function

class SnakeEnv(Environment):
    def __init__(self, size=10):
        # set the game_id
        self.game_id = str(uuid.uuid4())
        
        # set the size
        self.size = size

        # set the direction dictionary
        self.direction_dict = {
            SnakeAction.UP: (-1, 0),
            SnakeAction.RIGHT: (0, 1),
            SnakeAction.DOWN: (1, 0),
            SnakeAction.LEFT: (0, -1)
        }

        # set the reward function
        self.reward_function = reward_function

        # set the steps, and steps since last food
        self.steps = 0
        self.steps_since_last_food = 0

        # reset action history
        self.action_history = ActionHistory()
        
        # reset the environment
        self.reset()

    def place_food(self):
        # loop
        while True:
            # place the food somewhere randomly
            self.food = (random.randint(0, self.size-1), random.randint(0, self.size-1))

            # ensure the food is not in the snake
            if self.food not in self.snake:
                break

    def reset(self):
        # set the game_id
        self.game_id = str(uuid.uuid4())

        # no game over
        self.game_over = False

        # self.snake is essentially a list of grid coordinates for the snake
        # the snake always starts at the center of the grid i.e. [5,5]
        self.snake = [(self.size//2, self.size//2)]

        # place the food in the grid
        self.place_food()

        # Choose a random initial direction
        initial_action = random.choice([SnakeAction(SnakeAction.UP), SnakeAction(SnakeAction.RIGHT), SnakeAction(SnakeAction.DOWN), SnakeAction(SnakeAction.LEFT)])
        self.direction = self.direction_dict[initial_action.action]

        # set steps since last food
        self.steps = 0
        self.steps_since_last_food = 0

        # Reset the action history
        self.action_history.clear()

        # return the state
        return self.get_state()
    
    def get_next_head(self):
        # calculate the next position of the head without wrap around
        return (self.snake[-1][0] + self.direction[0], 
                self.snake[-1][1] + self.direction[1])

    def is_valid_direction_change(self, action: SnakeAction):
        """
        Check if the direction change is valid (not a 180-degree turn).
        """
        current_direction = next(key for key, value in self.direction_dict.items() if value == self.direction)
        if (current_direction == SnakeAction.UP and action.action == SnakeAction.DOWN) or \
           (current_direction == SnakeAction.DOWN and action.action == SnakeAction.UP) or \
           (current_direction == SnakeAction.LEFT and action.action == SnakeAction.RIGHT) or \
           (current_direction == SnakeAction.RIGHT and action.action == SnakeAction.LEFT):
            return False
        return True
    
    def is_valid_position(self, position):
        # get x,y from position
        x, y = position

        # ensure within bounds of grid
        return 0 <= x < self.size and 0 <= y < self.size
    
    def get_state(self):
        # set the state to zero
        state = np.zeros((self.size, self.size, 4))

        # channel 0: the snake body
        for i, j in self.snake:
            # set the snake body
            state[i, j, 0] = 1

        # channel 1: the snake head
        state[self.snake[-1][0], self.snake[-1][1], 1] = 1

        # channel 2: set the food
        state[self.food[0], self.food[1], 2] = 1

        # channel 3: Direction
        next_head = self.get_next_head()
        if self.is_valid_position(next_head):
            state[next_head[0], next_head[1], 3] = 1

        # return the state
        return state
    
    def step(self, action: SnakeAction = SnakeAction(SnakeAction.NONE)):
        # Ensure action is an instance of SnakeAction
        if not isinstance(action, SnakeAction):
            action = SnakeAction(action)

        # Determine the previous direction before applying the new action
        prev_direction = next(key for key, value in self.direction_dict.items() if value == self.direction)
        
        # Log the current state before updating
        self.action_history.add_record(
            step=self.steps,
            snake_head_position=self.snake[-1],
            snake_direction=prev_direction,
            snake_length=len(self.snake),
            action=action
        )

        # Update direction only if a new direction is specified
        if action.action != SnakeAction.NONE and self.is_valid_direction_change(action):
            self.direction = self.direction_dict[action.action]

        # get the next position
        new_head = self.get_next_head()
        
        # Check if snake has hit itself
        if not self.is_valid_position(new_head) or new_head in self.snake[:-1]:
            # game over
            self.game_over = True

            # return game state, reward, and game over
            return self.get_state(), self.reward_function(eaten=False, dead=True, steps=self.steps_since_last_food), self.game_over
        
        # Check if we took too many steps
        if self.steps_since_last_food > 100:
            # game over
            self.game_over = True

            # return game state, reward, and game over
            return self.get_state(), self.reward_function(eaten=False, dead=True, steps=self.steps_since_last_food), self.game_over

        # add the new head to the snake
        self.snake.append(new_head)
        
        # check if the snake ate the food
        eaten = new_head == self.food

        if eaten:
            # Place new food
            self.place_food()

            # set the reward
            reward = self.reward_function(eaten=True, dead=False, steps=self.steps_since_last_food)
            
            # Reset steps since last food eaten
            self.steps_since_last_food = 0
        else:
            # Remove the tail if food wasn't eaten
            self.snake.pop(0)

            # set the reward
            reward = self.reward_function(eaten=False, dead=False, steps=self.steps_since_last_food)

            # increase steps since last food
            self.steps_since_last_food += 1
        
        # increase steps
        self.steps += 1

        # return the state, reward and game over
        return self.get_state(), reward, self.game_over

    def get_render(self):
        # Set the grid as .'s
        grid = [['.' for _ in range(self.size)] for _ in range(self.size)]

        # Set the snake body position in the grid
        for i, j in self.snake[:-1]:  # All but the last segment (head)
            grid[i][j] = 'O'

        # Set the head of the snake (H) in the grid
        head_x, head_y = self.snake[-1]
        grid[head_x][head_y] = 'H'

        # Set the food position in the grid
        food_x, food_y = self.food
        grid[food_x][food_y] = 'F'

        # Convert grid to a string
        grid_str = '\n'.join([' '.join(row) for row in grid])

        # Get the current direction as a string
        current_direction_action = next(key for key, value in self.direction_dict.items() if value == self.direction)
        direction_str = str(SnakeAction(current_direction_action))

        # Prepare additional information
        legend = [
            "Legend:",
            " H - Head of the snake",
            " O - Body of the snake",
            " F - Food",
            " . - Empty space",
            ""
        ]

        game_state = [
            "Game State:",
            f" Score: {len(self.snake) - 1}",
            f" Current Direction: {direction_str}",
            f" Steps since last food: {self.steps_since_last_food}",
            f" Total steps: {self.steps}",
            f" Game over: {self.game_over}",
            f" Snake Length: {len(self.snake)}",
            f" Snake Head Position: {self.snake[-1]}",
            f" Snake Body Positions: {self.snake[:-1]}",
            f" Food Position: {self.food}"
        ]

        # Prepare action history
        action_history_str = ["\nAction History:"]
        for record in self.action_history.get_history():
            direction = str(SnakeAction(record['snake_direction']))
            action = str(SnakeAction(record['action'].action))
            action_history_str.append(
                f" Step: {record['step']}, Current Position: {record['snake_head_position']}, "
                f"Current Direction: {direction}, Snake Length: {record['snake_length']}, "
                f"Agent Chosen Action: {action}"
            )

        # Combine grid, legend, game state information, and action history
        render_str = "\n".join(legend) + "\n" + grid_str + "\n\n" + "\n".join(game_state) + "\n".join(action_history_str)

        return render_str

    def render(self):
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get and print the render string
        print(self.get_render())

    def get_action_history(self):
        return self.action_history.get_history()
