# File: snake_environment.py
import numpy as np
import os
import random
import uuid
from agents.snake.agent_action import AgentAction
from environments.environment_base import Environment
from environments.snake.reward_functions import simple_reward as reward_function

class SnakeEnv(Environment):
    def __init__(self, size=10):
        # set the game_id
        self.game_id = str(uuid.uuid4())
        
        # set the size
        self.size = size

        # set the direction dictionary
        self.direction_dict = {
            AgentAction.UP: (-1, 0),
            AgentAction.RIGHT: (0, 1),
            AgentAction.DOWN: (1, 0),
            AgentAction.LEFT: (0, -1)
        }

        # set the reward function
        self.reward_function = reward_function

        # set the steps, and steps since last food
        self.steps = 0
        self.steps_since_last_food = 0
        
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
        initial_action = random.choice([AgentAction.UP, AgentAction.RIGHT, AgentAction.DOWN, AgentAction.LEFT])
        self.direction = self.direction_dict[initial_action]

        # set steps since last food
        self.steps = 0
        self.steps_since_last_food = 0

        # return the state
        return self.get_state()
    
    def get_next_head(self):
        # calculate the next position of the head without wrap around
        return (self.snake[-1][0] + self.direction[0], 
                self.snake[-1][1] + self.direction[1])

    
    def is_valid_direction_change(self, action):
        """
        Check if the direction change is valid (not a 180-degree turn).
        """
        current_direction = next(key for key, value in self.direction_dict.items() if value == self.direction)
        if (current_direction == AgentAction.UP and action == AgentAction.DOWN) or \
           (current_direction == AgentAction.DOWN and action == AgentAction.UP) or \
           (current_direction == AgentAction.LEFT and action == AgentAction.RIGHT) or \
           (current_direction == AgentAction.RIGHT and action == AgentAction.LEFT):
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
    
    def step(self, action: AgentAction = AgentAction.NONE):
        # Update direction only if a new direction is specified
        if action != AgentAction.NONE and self.is_valid_direction_change(action):
            self.direction = self.direction_dict[action]

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
        
        # check if the snake ate the food
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

            # increase steps since last have food
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
        direction_str = next(key for key, value in self.direction_dict.items() if value == self.direction)

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

        # Combine grid, legend, and game state information
        render_str = "\n".join(legend) + "\n" + grid_str + "\n\n" + "\n".join(game_state)

        return render_str


    def render(self):
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get and print the render string
        print(self.get_render())
