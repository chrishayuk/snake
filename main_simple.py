# File: main_simple_cli.py
import os
import time
import argparse
from agents.agent_loader import get_agent
from environments.environment_loader import get_environment

# Function to get the application root
def get_app_root():
    return os.path.dirname(os.path.abspath(__file__))

def play(selected_env_id, selected_agent_id):
    # Create environment using the loader
    env, env_config = get_environment(selected_env_id)

    # Create agent using the loader
    agent, agent_config = get_agent(selected_agent_id)

    # get the initial state
    state = env.get_state()

    # Check compatibility
    if env_config['id'] not in agent_config['compatible_environments']:
        raise ValueError(f"The agent '{agent_config['name']}' is not compatible with the environment '{env_config['name']}'")

    # Display configuration details
    print(f"Environment ID: {env_config['id']}")
    print(f"Environment Name: {env_config['name']}")
    print(f"Environment Description: {env_config['description']}")

    print(f"Agent ID: {agent_config['id']}")
    print(f"Agent Name: {agent_config['name']}")
    print(f"Agent Description: {agent_config['description']}")

    # 1 second delay
    time.sleep(1)

    # loop for 1000 episodes
    for episode in range(1000):
        # render the environment
        env.render()

        # 150 millisecond delay
        time.sleep(0.15)

        # perform an action
        action = agent.get_action(state)
        state, reward, game_over = env.step(action)

        # break, if game over
        if game_over:
            # render the environment
            env.render()

            # 2 second delay
            time.sleep(2)

            # reset the environment
            env.reset()

            # 150 millisecond delay
            time.sleep(0.15)

def list_available_environments():
    #environments = list_environments()
    print("Available Environments:")
    #for env in environments:
    #    print(f"ID: {env['id']}, Name: {env['name']}, Description: {env['description']}")

def list_available_agents():
    #agents = list_agents()
    print("Available Agents:")
    #for agent in agents:
    #    print(f"ID: {agent['id']}, Name: {agent['name']}, Description: {agent['description']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the environment-agent simulation.")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for the play command
    play_parser = subparsers.add_parser("play", help="Run the simulation with specified environment and agent")
    play_parser.add_argument('--env', type=str, required=True, help="ID of the environment to use")
    play_parser.add_argument('--agent', type=str, required=True, help="ID of the agent to use")

    # Subparser for listing environments
    list_env_parser = subparsers.add_parser("list-environments", help="List available environments")

    # Subparser for listing agents
    list_agent_parser = subparsers.add_parser("list-agents", help="List available agents")

    args = parser.parse_args()

    if args.command == "play":
        play(args.env, args.agent)
    elif args.command == "list-environments":
        list_available_environments()
    elif args.command == "list-agents":
        list_available_agents()
    else:
        parser.print_help()
