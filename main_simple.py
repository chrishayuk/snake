import os
import time
import argparse
from agents import agent_loader
from agents.agent_loader import get_agent, list_agents, agent_loader 

from agents.agent_type import AgentType
from environments.environment_loader import get_environment, list_environments

# Function to get the application root
def get_app_root():
    return os.path.dirname(os.path.abspath(__file__))

# Get the agent list
def get_agents(game_id, env_config, selected_agents, providers=None, models=None):
    if isinstance(selected_agents, str):
        selected_agents = [selected_agents]

    agents = []
    llm_index = 0  # Keep track of the index for LLM agents only

    for agent_id in selected_agents:
        agent_params = {}

        # Get the agent config to determine if it's an LLM agent
        agent_config = agent_loader.get_agent_config(agent_id)

        if agent_config.agent_type == "LLM Agent":
            if providers and models:
                try:
                    # Use the llm_index to assign provider and model only to LLM agents
                    provider = providers[llm_index] if llm_index < len(providers) else None
                    model = models[llm_index] if llm_index < len(models) else None

                    if provider is None or model is None:
                        raise ValueError(f"Insufficient providers or models for LLM agent {agent_id}")

                    agent_params["provider"] = provider
                    agent_params["model_name"] = model

                    print(f"Assigning provider {provider} and model {model} to agent {agent_id}")
                    llm_index += 1  # Increment LLM index after successful assignment
                except IndexError as e:
                    print(f"Error: Not enough providers or models for LLM agent {agent_id}: {e}")
                    continue  # Skip this agent if provider or model is missing
        elif agent_config.agent_type == "Human":
            # Instantiate a Human agent
            agent = HumanTicTacToeAgent(id=agent_id, name=agent_config.name, description=agent_config.description)
            agent.game_id = game_id
            agents.append(agent)
        else:
            # Skip provider/model assignment for classic agents
            print(f"Skipping provider and model assignment for classic agent {agent_id}")

        print(f"Final agent_params being passed: {agent_params}")

        try:
            agent, agent_config = get_agent(agent_id, **agent_params)
            print(f"Agent {agent_id} instantiated successfully.")
        except TypeError as e:
            print(f"Failed to load agent {agent_id} with error: {e}")
            raise

        if env_config.id not in agent_config.compatible_environments:
            raise ValueError(f"Agent {agent_config.name} is not compatible with environment {env_config.name}")

        agent.game_id = game_id
        agents.append(agent)

    return agents



def play(selected_env_id, selected_agents, providers=None, models=None, episodes=1000):
    # Create environment using the loader
    env, env_config = get_environment(selected_env_id)

    # Get the agents and their types
    agents = get_agents(env.game_id, env_config, selected_agents, providers, models)

    # Set agents in the environment (for both SnakeEnv and TicTacToeEnv)
    if hasattr(env, 'set_agents'):
        env.set_agents(agents)

    # 1 second delay before starting
    time.sleep(1)

    # Loop for the specified number of episodes
    for episode in range(1, episodes + 1):
        print(f"\n=== Episode {episode} ===\n")

        # Reset the environment (this will handle player swapping)
        state = env.reset()

        # Make sure each agent has the correct game_id
        for agent in env.agents:
            agent.game_id = env.game_id

        # Render the environment initially
        env.render()

        # 150 millisecond delay
        time.sleep(0.15)

        # Loop until the game is over
        while not env.game_over:
            for agent in env.agents:
                # Ensure only the current player takes their turn
                if agent.player == env.current_player:
                    # Perform action based on agent type (LLM or classic)
                    if agent.agent_type == AgentType.LLM:
                        # Pass both the state and the rendered state
                        action = agent.get_action(env.steps + 1, state, env.get_render(), env.current_player)
                    else:
                        # Pass both the state and the rendered state
                        action = agent.get_action(env.steps + 1, state, env.get_render(), env.current_player)

                    # Now perform a step in the environment
                    state, reward, game_over = env.step(action, agent)

                    # **Render after every step** to reflect the current state
                    env.render()

                    # Break if the game is over
                    if game_over:
                        break

                    # 150 millisecond delay between actions
                    time.sleep(0.15)
                else:
                    # error
                    print(f"Skipping agent {agent.unique_agent_id}, it's not their turn.")

                    # 150 millisecond delay between actions
                    time.sleep(0.15)

            # Break the outer loop if the game is over
            if env.game_over:
                break


        # Render the environment at the end of the episode as well
        env.render()

        # 2 second delay
        time.sleep(2)

        # Perform game over actions for all agents
        for agent in env.agents:
            # game over
            agent.game_over(env.steps + 1, state, env.get_render())

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
