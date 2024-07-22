import time
import numpy as np
from agents.snake.dqn_agent import DQNAgent
from environments.environment_loader import get_environment

def train_dqn(episodes=10000, batch_size=32, render=False):
    # Example: Select Snake Environment
    selected_env_id = "snake_env_v1"

    # Create environment using the loader
    env, env_config = get_environment(selected_env_id)

    # get the state space
    state_dim = np.prod(env.get_state().shape)

    # setup our agent
    agent = DQNAgent(state_dim)
    
    for episode in range(episodes):
        # reset the environment
        state = env.reset()

        # reset the counters
        total_reward = 0
        steps = 0

        # we'll watch how it does every 300 steps
        if episode%5000 == 0:
            render = True
        else:
            render = False
        
        while True:
            if render:
                # render
                env.render()

                # 150 millisecond delate
                time.sleep(0.15)
            
            action = agent.get_action(state.flatten())
            next_state, reward, done = env.step(action)
            
            agent.remember(state.flatten(), action, reward, next_state.flatten(), done)
            
            state = next_state
            total_reward += reward
            steps += 1
            
            if len(agent.memory) > batch_size:
                agent.train(batch_size)
            
            if done:
                break
        
        print(f"Episode: {episode+1}/{episodes}, Score: {total_reward}, Steps: {steps}, Epsilon: {agent.epsilon:.2f}")
        
    return agent

if __name__ == "__main__":
    print("Starting training...")
    trained_agent = train_dqn(episodes=50000, render=False)
    print("Training completed!")