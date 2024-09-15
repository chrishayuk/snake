import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque
from agents.snake.snake_action import SnakeAction

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)  # Ensure this matches the flattened state size
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class PrioritizedReplayBuffer:
    def __init__(self, capacity, alpha=0.6):
        self.capacity = capacity
        self.alpha = alpha
        self.memory = []
        self.priorities = deque(maxlen=capacity)
        self.pos = 0

    def add(self, experience, error):
        max_priority = max(self.priorities) if self.memory else 1.0
        if len(self.memory) < self.capacity:
            self.memory.append(experience)
        else:
            self.memory[self.pos] = experience

        self.priorities.append(max_priority)
        self.pos = (self.pos + 1) % self.capacity

    def sample(self, batch_size, beta=0.4):
        priorities = np.array(self.priorities)
        probabilities = priorities ** self.alpha
        probabilities /= probabilities.sum()

        indices = np.random.choice(len(self.memory), batch_size, p=probabilities)
        experiences = [self.memory[i] for i in indices]

        total = len(self.memory)
        weights = (total * probabilities[indices]) ** (-beta)
        weights /= weights.max()
        return experiences, indices, np.array(weights, dtype=np.float32)

    def update_priorities(self, indices, errors):
        for idx, error in zip(indices, errors):
            self.priorities[idx] = abs(error) + 1e-5  # Ensure non-zero priority

class DQNAgent:
    def __init__(self, state_dim, learning_rate=1e-4, gamma=0.99, epsilon=1.0, epsilon_decay=0.9995, epsilon_min=0.1, buffer_size=100000, alpha=0.6, beta_start=0.4):
        self.state_dim = state_dim
        self.action_dim = 4  # UP, RIGHT, DOWN, LEFT
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Initialize networks
        self.model = DQN(state_dim, self.action_dim).to(self.device)
        self.target_model = DQN(state_dim, self.action_dim).to(self.device)
        self.update_target_model()

        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()

        # Prioritized Experience Replay buffer
        self.memory = PrioritizedReplayBuffer(buffer_size, alpha)
        self.beta = beta_start

        self.action_map = {
            0: SnakeAction.UP,
            1: SnakeAction.RIGHT,
            2: SnakeAction.DOWN,
            3: SnakeAction.LEFT
        }
        self.reverse_action_map = {v: k for k, v in self.action_map.items()}

        # Reward tracking
        self.reward = 0

    def get_action(self, step: int, state, valid_actions):
        """Select an action using an epsilon-greedy strategy and a list of valid actions."""
        if np.random.rand() <= self.epsilon:
            return random.choice(valid_actions)  # Only pick from valid actions
        
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        q_values = self.model(state)
        
        # Filter the Q-values based on valid actions only
        valid_action_indices = [self.reverse_action_map[a] for a in valid_actions]
        valid_q_values = q_values[0, valid_action_indices]
        
        # Select the action with the highest Q-value from the valid set
        best_action_index = torch.argmax(valid_q_values).item()
        return valid_actions[best_action_index]


    def remember(self, state, action, reward, next_state, done, error=1.0):
        """Store experiences in the replay buffer with priority."""
        action_int = self.reverse_action_map[action]  # Convert action to integer
        self.memory.add((state, action_int, reward, next_state, done), error)

    def train(self, batch_size=32, beta=0.4):
        if len(self.memory.memory) < batch_size:
            return
        
        experiences, indices, weights = self.memory.sample(batch_size, beta)
        states, actions, rewards, next_states, dones = map(np.array, zip(*experiences))

        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)
        weights = torch.FloatTensor(weights).to(self.device)

        # Get the next actions using the main model
        next_actions = self.model(next_states).argmax(1).unsqueeze(1)
        
        # Use the target model to calculate next Q-values
        next_q_values = self.target_model(next_states).gather(1, next_actions).squeeze(1).detach()

        target_q_values = rewards + (1 - dones) * self.gamma * next_q_values
        current_q_values = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)

        td_errors = (current_q_values - target_q_values).detach().cpu().numpy()
        self.memory.update_priorities(indices, td_errors)

        loss = (self.criterion(current_q_values, target_q_values) * weights).mean()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_model(self):
        """Copy weights from model to target_model."""
        self.target_model.load_state_dict(self.model.state_dict())

    def add_reward(self, reward):
        """Add a reward to the agent's total."""
        self.reward += reward

    def reset_reward(self):
        """Reset the reward at the start of a new game."""
        self.reward = 0

    def load(self, name):
        """Load a model's state dictionary."""
        self.model.load_state_dict(torch.load(name))

    def save(self, name):
        """Save the model's state dictionary."""
        torch.save(self.model.state_dict(), name)
