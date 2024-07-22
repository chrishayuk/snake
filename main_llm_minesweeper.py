# File: main_llm_minesweeper.py
import numpy as np
import time
from agents.minesweeper.llm_agent import LLMAgent
from environments.environment_loader import get_environment
from agents.minesweeper.agent_action import MinesweeperAction

def parse_action(agent_action):
    print(f"Agent action: {agent_action}")
    try:
        action = MinesweeperAction.from_string(str(agent_action))
        return action.row, action.col, action.action_type == MinesweeperAction.ActionType.FLAG
    except ValueError as e:
        print(f"Invalid action: {e}")
        return None, None, None

def run_episode(env, agent, render=True, delay=0.15):
    state = env.reset()
    total_reward = 0
    steps = 0

    while True:
        if render:
            env.render()
            time.sleep(delay)

        # get the state as a string
        render = env.get_render()

        # perform an action
        agent_action = agent.get_action(render)
        
        # parse the action
        row, col, is_flag = parse_action(agent_action)
        
        if row is None or col is None:
            print("Debug: Invalid action returned by agent")
            continue

        # take a step in the environment
        state, reward, game_over = env.step((row, col, is_flag))

        total_reward += reward
        steps += 1

        print(f"Step: {steps}, Action: {'Flag' if is_flag else 'Reveal'} ({row}, {col}), Reward: {reward}")
        print(f"Revealed: {np.sum(env.revealed)}, Flagged: {np.sum(env.flagged)}, Game over: {game_over}, Win: {env.win}")

        if game_over:
            if render:
                env.render()
                time.sleep(0.5)
            print("Debug: Game over reached")
            break

    return total_reward, steps, env.win

def main():
    # Example: Select Minesweeper Environment
    selected_env_id = "minesweeper_env_v1"

    # Create environment using the loader
    env, env_config = get_environment(selected_env_id)

    # create our LLM agent
    #agent = LLMAgent("openai", "gpt-4o")
    #agent = LLMAgent("openai", "gpt-4o-mini")
    agent = LLMAgent("ollama", "gemma2:27b")
    #agent = LLMAgent("anthropic", "claude-3-5-sonnet")

    num_episodes = 10  # Reduced for testing, increase as needed
    total_wins = 0
    total_steps = 0
    total_reward = 0

    for episode in range(num_episodes):
        print(f"\nStarting Episode {episode + 1}")
        episode_reward, episode_steps, win = run_episode(env, agent, render=True, delay=0.15)
        
        total_wins += int(win)
        total_steps += episode_steps
        total_reward += episode_reward

        print(f"Episode {episode + 1}: Reward = {episode_reward}, Steps = {episode_steps}, Win = {win}")

    print(f"\nTest Results:")
    print(f"Total Episodes: {num_episodes}")
    print(f"Wins: {total_wins}")
    print(f"Win Rate: {total_wins / num_episodes:.2%}")
    print(f"Average Steps: {total_steps / num_episodes:.2f}")
    print(f"Average Reward: {total_reward / num_episodes:.2f}")

if __name__ == "__main__":
    main()