import time
import numpy as np
import torch
from agents.snake.dqn_agent import DQNAgent
from environments.environment_loader import get_environment

def train_dqn(episodes=10000, batch_size=64, render_interval=500, render_delay=0.1):
    """ Train the DQN agent for a given number of episodes """
    # Example: Select Snake Environment
    selected_env_id = "snake"

    # Create environment using the loader
    env, env_config = get_environment(selected_env_id)

    # Get the state space (ensure it is flattened)
    state_dim = np.prod(env.get_state().shape)

    # Setup our agent
    agent = DQNAgent(state_dim)

    for episode in range(episodes):
        # Reset the environment and the agent's reward
        state = env.reset()

        # Ensure the state is flattened before passing it to the agent
        state = state.flatten()

        # resent the agent reward
        agent.reset_reward()

        # Reset the counters
        steps = 0

        # Determine if we should render this episode based on the render interval
        render = True if episode % render_interval == 0 else False
        
        while True:
            if render:
                # Render the environment on every step
                env.render()

                # 150 millisecond delay between actions
                time.sleep(0.15)

            # Get valid actions from the environment
            valid_actions = env.get_valid_actions()

            # Get the action from the agent, only using valid actions
            action = agent.get_action(steps, state, valid_actions=valid_actions)

            # Perform the action and get the new state and reward
            next_state, reward, done = env.step(action, agent=agent)

            # Ensure the next state is also flattened
            next_state = next_state.flatten()

            # Calculate TD error (for prioritized replay)
            with torch.no_grad():
                next_q_value = agent.target_model(torch.FloatTensor(next_state).unsqueeze(0).to(agent.device)).max().item()
                
                # Get the Q-values from the model for the current state
                q_values = agent.model(torch.FloatTensor(state).unsqueeze(0).to(agent.device))

                # Index the Q-value for the chosen action
                current_q_value = q_values[0, agent.reverse_action_map[action]].item()

                td_error = abs(reward + (1 - done) * agent.gamma * next_q_value - current_q_value)

            # Store the experience in the agent's memory
            agent.remember(state, action, reward, next_state, done, error=td_error)

            # Update the current state
            state = next_state
            steps += 1

            # Train the agent if enough experiences are stored
            if len(agent.memory.memory) > batch_size:
                agent.train(batch_size, beta=min(1.0, agent.beta + 0.001))  # Increase beta gradually

            # End the episode if the game is done
            if done:
                break
        
        # Update the target network every 10 episodes
        if episode % 10 == 0:
            agent.update_target_model()

        # Print episode statistics
        print(f"Episode: {episode+1}/{episodes}, Total Reward: {agent.reward}, Steps: {steps}, Epsilon: {agent.epsilon:.2f}")

    return agent


if __name__ == "__main__":
    print("Starting training...")
    trained_agent = train_dqn(episodes=50000, render_interval=500, render_delay=0.1)
    print("Training completed!")
