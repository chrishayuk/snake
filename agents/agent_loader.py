import os
import json
import importlib
from typing import Any, List, Tuple
from agents.agent_config import AgentConfig

class AgentLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.agent_configs = self.load_configs()

    def load_configs(self) -> List[dict]:
        with open(self.config_path) as f:
            return json.load(f)

    def get_agent_config(self, agent_id) -> AgentConfig:
        for agent_config in self.agent_configs:
            if agent_config['id'] == agent_id:
                return AgentConfig(**agent_config)
        raise ValueError(f"Agent with id '{agent_id}' not found")

    def load_class(self, full_class_string: str) -> Any:
        module_path, class_name = full_class_string.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    def get_agent(self, id: str, **kwargs) -> Tuple[Any, AgentConfig]:
        # Get the agent config from the config file
        agent_config = self.get_agent_config(id)

        # Initialize agent_params from the config
        agent_params = agent_config.agent_params.copy()  # Ensure we don't modify the original

        # Overwrite config params with any kwargs passed in
        for key, value in kwargs.items():
            if key in ['provider', 'model_name']:  # Explicitly check for these keys
                agent_params[key] = value

        # Debugging output to see the parameters passed to the agent
        print(f"Instantiating agent {id} with parameters: {agent_params}")

        # Load the agent class
        AgentClass = self.load_class(agent_config.agent)

        # Ensure the required parameters are passed correctly
        try:
            # Instantiate the agent, passing id, name, description, and additional parameters
            agent_instance = AgentClass(
                id=agent_config.id,
                name=agent_config.name,
                description=agent_config.description,
                **agent_params
            )
        except TypeError as e:
            raise TypeError(f"Error while instantiating agent {id}: {e}")

        # Return the agent instance and the agent config
        return agent_instance, agent_config


    def list_agents(self) -> List[AgentConfig]:
        # list the agents
        return [AgentConfig(**agent_config) for agent_config in self.agent_configs]

# Function to get the application root
def get_app_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app_root = get_app_root()
agent_loader = AgentLoader(os.path.join(app_root, 'config', 'agent_config.json'))

def get_agent(id: str, **kwargs) -> Tuple[Any, AgentConfig]:
    # get the agent by id with dynamic parameters
    return agent_loader.get_agent(id, **kwargs)

def list_agents() -> List[AgentConfig]:
    # list the agents
    return agent_loader.list_agents()
