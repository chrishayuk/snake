# File: main_llm.py
import time
from agents.llm_agent import LLMAgent
from snake_environment import SnakeEnv

# setup the environment
env = SnakeEnv(size=10)

# create our LLM agent
#agent = LLMAgent("openai", "gpt-4o")
#agent = LLMAgent("openai", "gpt-4o-mini")
agent = LLMAgent("ollama", "llama3:70b")
#agent = LLMAgent("anthropic", "claude-3-5-sonnet")

# loop for 1000 episodes
for episode in range(1000):
    # get the state
    render = env.get_render()

    # render the environment
    env.render()

    # 150 millisecond delay
    time.sleep(0.15)

    # perform an action
    action = agent.get_action(render)
    state, reward, game_over = env.step(action)

    # break, if game over
    if game_over:
        # render the environment
        env.render()

        # 500 millisecond delay
        time.sleep(0.5)

        # reset the environment
        state = env.reset()

        # 150 millisecond delay
        time.sleep(0.15)

    print(f"Episode: {episode}, Reward: {reward}")