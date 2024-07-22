import os
import json
import importlib
from typing import Any, List, Tuple
from agents.agent_type import AgentType

class AgentLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.agent_configs = self.load_configs()

    def load_configs(self) -> List[dict]:
        with open(self.config_path) as f:
            return json.load(f)

    def get_agent_config(self, agent_id) -> AgentType:
        for agent_config in self.agent_configs:
            if agent_config['id'] == agent_id:
                return AgentType(**agent_config)
        raise ValueError(f"Agent with id '{agent_id}' not found")

    def load_class(self, full_class_string: str) -> Any:
        module_path, class_name = full_class_string.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    def get_agent(self, agent_id: str) -> Tuple[Any, AgentType]:
        # get the agent config
        agent_config = self.get_agent_config(agent_id)

        # load the agent class
        AgentClass = self.load_class(agent_config.agent)

        # instantiate the instance, setting the agent id etc
        agent_instance = AgentClass(
            agent_id=agent_config.id,
            name=agent_config.name,
            description=agent_config.description,
            **agent_config.agent_params
        )

        # return the instance and config
        return agent_instance, agent_config

    def list_agents(self) -> List[AgentType]:
        # list the agents
        return [AgentType(**agent_config) for agent_config in self.agent_configs]

# Function to get the application root
def get_app_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app_root = get_app_root()
agent_loader = AgentLoader(os.path.join(app_root, 'config', 'agent_config.json'))

def get_agent(agent_id: str) -> Tuple[Any, AgentType]:
    return agent_loader.get_agent(agent_id)

def list_agents() -> List[AgentType]:
    return agent_loader.list_agents()
