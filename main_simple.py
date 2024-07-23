import os
import time
import argparse
from agents.agent_loader import get_agent, list_agents
from agents.agent_type import AgentType
from environments.environment_loader import get_environment, list_environments

# Function to get the application root
def get_app_root():
    return os.path.dirname(os.path.abspath(__file__))

def play(selected_env_id, selected_agent_id):
    # Create environment using the loader
    env, env_config = get_environment(selected_env_id)

    # Create agent using the loader
    agent, agent_config = get_agent(selected_agent_id)

    # Ensure that the environment is compatible with the agent
    if env_config.id not in agent_config.compatible_environments:
        raise ValueError(f"Agent {agent_config.name} is not compatible with environment {env_config.name}")

    # 1 second delay
    time.sleep(1)

    # Initialize state
    state = env.reset()

    # set the game id
    agent.game_id = env.game_id

    # loop for 1000 episodes
    for episode in range(1000):
        # render the environment
        env.render()

        # 150 millisecond delay
        time.sleep(0.15)

        # perform an action
        if agent.agent_type == AgentType.LLM:
            # we're dealing with an LLM, so use the render
            action = agent.get_action(env.get_render())
        else:
            # classic agent, so use the state
            action = agent.get_action(state)
        
        # now perform a step
        state, reward, game_over = env.step(action)

        # break, if game over
        if game_over:
            # render the environment
            env.render()

            # 2 second delay
            time.sleep(2)

            # reset the environment
            state = env.reset()

            # set the game id
            agent.game_id = env.game_id

            # 150 millisecond delay
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
