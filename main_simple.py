# File: main_simple.py
import os
import time
from agents.snake.smart_seeker_agent import SmartSeekerAgent
from environments.environment_loader import get_environment

# Function to get the application root
def get_app_root():
    return os.path.dirname(os.path.abspath(__file__))

# Example: Select Snake Environment
selected_env_id = "snake_env_v1"

# Create environment using the loader
env, env_config = get_environment(selected_env_id)

# get the initial state
state = env.get_state()

# create our agent
#agent = FoodSeekerAgent()
agent = SmartSeekerAgent()
#agent = HamiltonianAgent(10)
#agent = AdaptiveHamiltonianAgent([10,10])

# loop for 1000 episodes
for episode in range(1000):
    # render the environment
    env.render()

    # 150 millisecond delate
    time.sleep(0.15)

    # perform an action
    action = agent.get_action(state)
    state, reward, game_over = env.step(action)

    # break, if game over
    if game_over:
        # render the environment
        env.render()

        # 150 millisecond delate
        time.sleep(0.5)

        # reset the environment
        env.reset()

        # 150 millisecond delate
        time.sleep(0.15)