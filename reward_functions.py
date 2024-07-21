# File: reward_functions.py
def simple_reward(eaten, dead, steps):
    if dead:
        return -1
    elif eaten:
        return 1
    elif steps > 49:
        return -1
    else:
        return 0
    
# def improved_reward(eaten, dead, steps, repeated_action):
#     if dead:
#         # High penalty for dying
#         return -100  
#     elif eaten:
#         # Reward for eating, with bonus for efficiency
#         return 50 + (100 / (steps + 1))  
#     else:
#         # Small positive reward for surviving
#         survival_reward = 0.1
        
#         # Reward for getting closer to food
#         distance_reward = 1 / (distance_to_food + 1)
        
#         # Penalty for repeating the same action
#         repetition_penalty = -1 if repeated_action else 0
        
#         # balance it all out
#         return survival_reward + distance_reward + repetition_penalty