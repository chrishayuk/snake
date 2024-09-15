# File: reward_functions.py
import numpy as np

def simple_reward(eaten, dead, steps):
    if dead:
        return -1
    elif eaten:
        return 1
    elif steps > 49:
        return -1
    else:
        return 0
    
def improved_reward(eaten, dead, steps, repeated_action, snake_head, food_position):
    if dead:
        # High penalty for dying
        return -100
    elif eaten:
        # Reward for eating, with bonus for efficiency
        return 50 + (100 / (steps + 1))
    else:
        # Small positive reward for surviving
        survival_reward = 0.1

        # Calculate Manhattan distance to the food
        distance_to_food = np.abs(snake_head[0] - food_position[0]) + np.abs(snake_head[1] - food_position[1])

        # Reward for getting closer to food (larger reward the closer it gets)
        distance_reward = 1 / (distance_to_food + 1)

        # Penalty for repeating the same action
        repetition_penalty = -1 if repeated_action else 0

        # Combine rewards and penalties
        return survival_reward + distance_reward + repetition_penalty