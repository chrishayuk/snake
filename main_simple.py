# File: main_simple.py
import os
import time
from agents.agent_loader import get_agent
from environments.environment_loader import get_environment

# Function to get the application root
def get_app_root():
    return os.path.dirname(os.path.abspath(__file__))

# select the environment and agent
selected_env_id = "snake_env_v1"
selected_agent_id = "smart_seeker_v1"

# Create environment using the loader
env, env_config = get_environment(selected_env_id)

# Create agent using the loader
agent, agent_config = get_agent(selected_agent_id)

# get the initial state
state = env.get_state()

# Check compatibility
if env_config['id'] not in agent_config['compatible_environments']:
    raise ValueError(f"The agent '{agent_config['name']}' is not compatible with the environment '{env_config['name']}'")

# Display configuration details
print(f"Environment ID: {env_config['id']}")
print(f"Environment Name: {env_config['name']}")
print(f"Environment Description: {env_config['description']}")

print(f"Agent ID: {agent_config['id']}")
print(f"Agent Name: {agent_config['name']}")
print(f"Agent Description: {agent_config['description']}")

# 1 second delay
time.sleep(1)

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