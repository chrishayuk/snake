# File: main_llm.py
import time
from agents.snake.llm_agent import LLMAgent
from environments.environment_loader import get_environment

# Example: Select Snake Environment
selected_env_id = "snake_env_v1"

# Create environment using the loader
env, env_config = get_environment(selected_env_id)

# create our LLM agent
#agent = LLMAgent("openai", "gpt-4o")
#agent = LLMAgent("openai", "gpt-4o-mini")
agent = LLMAgent("ollama", "llama3")
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