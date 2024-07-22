# File: main_test_minesweeper.py
import time
import numpy as np
from agents.minesweeper.test_agent import TestAgent
from agents.minesweeper.agent_action import MinesweeperAction
from environments.environment_loader import get_environment

def run_test_episode(env, agent, render=True, delay=0.1):
    state = env.reset()
    agent.reset()  # Reset the agent for each episode
    total_reward = 0
    steps = 0

    while True:
        if render:
            env.render()
            time.sleep(delay)

        action = agent.get_action(state)
        if action is None:
            print("Debug: Agent returned None action")
            break

        state, reward, game_over = env.step((action.row, action.col, action.action_type == MinesweeperAction.ActionType.FLAG))
        
        revealed = np.argwhere(state[:,:,0] & ~env.flagged)
        agent.update(action, revealed)

        total_reward += reward
        steps += 1

        print(f"Step: {steps}, Action: {action.action_type.value} ({action.row}, {action.col}), Reward: {reward}")
        print(f"Revealed: {np.sum(env.revealed)}, Flagged: {np.sum(env.flagged)}, Game over: {game_over}, Win: {env.win}")

        if game_over:
            if render:
                env.render()
                time.sleep(delay)
            print("Debug: Game over reached")
            break

    return total_reward, steps, env.win

def main():
    size = 10
    num_mines = 10
    num_episodes = 100

    # Example: Select Minesweeper Environment
    selected_env_id = "minesweeper_env"

    # Create environment using the loader
    env, env_config = get_environment(selected_env_id)

    agent = TestAgent(size)

    wins = 0
    total_steps = 0
    total_reward = 0

    for episode in range(num_episodes):
        print(f"\nStarting Episode {episode + 1}")
        episode_reward, episode_steps, win = run_test_episode(env, agent, render=True, delay=0.1)
        
        wins += int(win)
        total_steps += episode_steps
        total_reward += episode_reward

        print(f"Episode {episode + 1}: Reward = {episode_reward}, Steps = {episode_steps}, Win = {win}")

        if episode >= 10:  # Stop after 10 episodes for debugging
            break

    print(f"\nTest Results:")
    print(f"Total Episodes: {episode + 1}")
    print(f"Wins: {wins}")
    print(f"Win Rate: {wins / (episode + 1):.2%}")
    print(f"Average Steps: {total_steps / (episode + 1):.2f}")
    print(f"Average Reward: {total_reward / (episode + 1):.2f}")

if __name__ == "__main__":
    main()