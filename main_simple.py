import os
import time
import argparse
from agents.agent_loader import get_agent, list_agents
from agents.agent_type import AgentType
from environments.environment_loader import get_environment, list_environments

# Function to get the application root
def get_app_root():
    return os.path.dirname(os.path.abspath(__file__))

def play(selected_env_id, selected_agents, providers=None, models=None, episodes=1000):
    # Convert single agent string to a list if only one agent is provided
    if isinstance(selected_agents, str):
        selected_agents = [selected_agents]

    # Create environment using the loader
    env, env_config = get_environment(selected_env_id)

    # Check if the environment supports the number of agents provided
    num_agents = len(selected_agents)
    if env_config.max_players and num_agents > env_config.max_players:
        raise ValueError(f"Too many agents provided! Environment {env_config.name} supports a maximum of {env_config.max_players} players.")
    elif env_config.min_players and num_agents < env_config.min_players:
        raise ValueError(f"Not enough agents provided! Environment {env_config.name} requires at least {env_config.min_players} players.")

    # Initialize agents
    agents = []
    for i, agent_id in enumerate(selected_agents):
        agent_params = {}
        if providers and i < len(providers) and models and i < len(models):
            agent_params = {"provider": providers[i], "model_name": models[i]}
        agent, agent_config = get_agent(agent_id, **agent_params)

        # Ensure that the environment is compatible with the agent
        if env_config.id not in agent_config.compatible_environments:
            raise ValueError(f"Agent {agent_config.name} is not compatible with environment {env_config.name}")

        # Set the game id for the agent and append to the agent list
        agent.game_id = env.game_id
        agents.append(agent)

    # 1 second delay before starting
    time.sleep(1)

    # Initialize state
    state = env.reset()

    # Loop for the specified number of episodes
    for episode in range(episodes):
        # Render the environment
        env.render()

        # 150 millisecond delay
        time.sleep(0.15)

        # Loop through agents in turns
        for agent in agents:
            # Perform action based on agent type (LLM or classic)
            if agent.agent_type == AgentType.LLM:
                action = agent.get_action(env.steps + 1, env.get_render())
            else:
                action = agent.get_action(env.steps + 1, state)

            # Now perform a step in the environment
            state, reward, game_over = env.step(action)

            # Break if the game is over
            if game_over:
                # Render the environment
                env.render()

                # 2 second delay
                time.sleep(2)

                # Perform game over actions for all agents
                for agent in agents:
                    if agent.agent_type == AgentType.LLM:
                        agent.game_over(env.steps + 1, env.get_render())
                    else:
                        agent.game_over(env.steps + 1, state)

                # Reset the environment
                state = env.reset()

                # Set the game id for all agents
                for agent in agents:
                    agent.game_id = env.game_id

                # Break out of the inner loop to reset the episode
                break

            # 150 millisecond delay between actions
            time.sleep(0.15)

def list_available_environments():
    environments = list_environments()
    print("Available Environments:")
    for env in environments:
        print(f"{env.id} - {env.description}")

def list_available_agents():
    agents = list_agents()
    print("Available Agents:")
    for agent in agents:
       print(f"{agent.id} - {agent.description}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the environment-agent simulation.")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for the play command
    play_parser = subparsers.add_parser("play", help="Run the simulation with specified environment and agents")
    play_parser.add_argument('--env', type=str, required=True, help="ID of the environment to use")
    play_parser.add_argument('--agents', type=str, nargs='+', required=True, help="List of agent IDs to use")
    play_parser.add_argument('--providers', type=str, nargs='*', help="List of providers for LLM agents")
    play_parser.add_argument('--models', type=str, nargs='*', help="List of model names for LLM agents")
    play_parser.add_argument('--episodes', type=int, default=1000, help="Number of episodes to run")

    # Subparser for listing environments
    list_env_parser = subparsers.add_parser("list-environments", help="List available environments")

    # Subparser for listing agents
    list_agent_parser = subparsers.add_parser("list-agents", help="List available agents")

    args = parser.parse_args()

    if args.command == "play":
        play(args.env, args.agents, args.providers, args.models, args.episodes)
    elif args.command == "list-environments":
        list_available_environments()
    elif args.command == "list-agents":
        list_available_agents()
    else:
        parser.print_help()

