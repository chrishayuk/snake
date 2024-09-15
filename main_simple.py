import os
import time
import argparse
from agents.agent_loader import get_agent, list_agents
from agents.agent_type import AgentType
from environments.environment_loader import get_environment, list_environments

# Function to get the application root
def get_app_root():
    return os.path.dirname(os.path.abspath(__file__))

# Get the agent list
def get_agents(game_id, env_config, selected_agents, providers=None, models=None):
    # Convert single agent string to a list if only one agent is provided
    if isinstance(selected_agents, str):
        selected_agents = [selected_agents]

    # Check if the environment supports the number of agents provided
    num_agents = len(selected_agents)

    # Check if the game supports the number of players
    if env_config.max_players and num_agents > env_config.max_players:
        raise ValueError(f"Too many agents provided! Environment {env_config.name} supports a maximum of {env_config.max_players} players.")
    elif env_config.min_players and num_agents < env_config.min_players:
        raise ValueError(f"Not enough agents provided! Environment {env_config.name} requires at least {env_config.min_players} players.")

    # Initialize agents
    agents = []

    # Loop through the agents
    for i, agent_id in enumerate(selected_agents):
        agent_params = {}
        if providers and i < len(providers) and models and i < len(models):
            agent_params = {"provider": providers[i], "model_name": models[i]}
        agent, agent_config = get_agent(agent_id, **agent_params)

        # Ensure that the environment is compatible with the agent
        if env_config.id not in agent_config.compatible_environments:
            raise ValueError(f"Agent {agent_config.name} is not compatible with environment {env_config.name}")

        # Set the game id for the agent and append to the agent list
        agent.game_id = game_id
        agents.append(agent)

    # Return agents and their types
    return agents

def play(selected_env_id, selected_agents, providers=None, models=None, episodes=1000):
    # Create environment using the loader
    env, env_config = get_environment(selected_env_id)

    # Get the agents and their types
    agents = get_agents(env.game_id, env_config, selected_agents, providers, models)

    # Set agents in the environment (environment now handles swapping)
    if hasattr(env, 'set_agents'):
        env.set_agents(agents)

    # 1 second delay before starting
    time.sleep(1)

    # Loop for the specified number of episodes
    for episode in range(1, episodes + 1):
        print(f"\n=== Episode {episode} ===\n")
        # Reset the environment (this will handle player swapping)
        state = env.reset()

        # Render the environment
        env.render()

        # 150 millisecond delay
        time.sleep(0.15)

        # Loop until the game is over
        while not env.game_over:
            for agent in env.agents:
                # Perform action based on agent type (LLM or classic)
                if agent.agent_type == AgentType.LLM:
                    # Get the action to perform from the LLM agent using the render function
                    action = agent.get_action(env.steps + 1, env.get_render())
                else:
                    # Get the action to perform the classic agent, using the state
                    action = agent.get_action(env.steps + 1, state)

                # Now perform a step in the environment
                state, reward, game_over = env.step(action)

                # Break if the game is over
                if game_over:
                    break

                # 150 millisecond delay between actions
                time.sleep(0.15)

            # Break the outer loop if the game is over
            if env.game_over:
                break

        # Render the environment
        env.render()

        # 2 second delay
        time.sleep(2)

        # Perform game over actions for all agents
        for agent in env.agents:
            if agent.agent_type == AgentType.LLM:
                agent.game_over(env.steps + 1, env.get_render())
            else:
                agent.game_over(env.steps + 1, state)

        # Continue to the next episode (game)

def list_available_environments():
    # Get the list of environments
    environments = list_environments()

    # Print the available environments
    print("Available Environments:")
    for env in environments:
        # Print the id and description
        print(f"{env.id} - {env.description}")

def list_available_agents():
    # Get the list of agents
    agents = list_agents()

    # Print the agents
    print("Available Agents:")
    for agent in agents:
       # Agent id and description
       print(f"{agent.id} - {agent.description}")

if __name__ == "__main__":
    # Setup the parser
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

    # Parse arguments
    args = parser.parse_args()

    if args.command == "play":
        # Play
        play(args.env, args.agents, args.providers, args.models, args.episodes)
    elif args.command == "list-environments":
        # List available environments
        list_available_environments()
    elif args.command == "list-agents":
        # List available agents
        list_available_agents()
    else:
        # Print help
        parser.print_help()
