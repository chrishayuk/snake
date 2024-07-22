# File: main_simple.py
import time
from agents.simple_agent import SimpleAgent
from snake_environment import SnakeEnv

# setup the environment
env = SnakeEnv(size=10)

# get the initial state
state = env.get_state()

# create our agent
agent = SimpleAgent()

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