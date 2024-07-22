# File: app/agents/agent_loader.py
import os
import json
import importlib

class AgentLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.agent_configs = self.load_configs()

    def load_configs(self):
        # load the agent agent config
        with open(self.config_path) as f:
            return json.load(f)

    def get_agent_config(self, agent_id):
        # loop through the agent configs
        for agent_config in self.agent_configs:
            # find the agent that matches
            if agent_config['id'] == agent_id:
                # return the matching agent config
                return agent_config
            
        # no matching agent
        raise ValueError(f"Agent with id '{agent_id}' not found")

    def load_class(self, full_class_string):
        module_path, class_name = full_class_string.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    def get_agent(self, agent_id):
        # get the agent config
        agent_config = self.get_agent_config(agent_id)

        # load the agent class
        AgentClass = self.load_class(agent_config['agent'])

        # instatiate the agent
        agent_instance = AgentClass(**agent_config.get('agent_params', {}))

        # return the agent
        return agent_instance, agent_config

# Function to get the application root
def get_app_root():
    # return the app root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create a global instance of AgentLoader for ease of use
app_root = get_app_root()
agent_loader = AgentLoader(os.path.join(app_root, 'config', 'agent_config.json'))

def get_agent(agent_id):
    # return the agent from it's id
    return agent_loader.get_agent(agent_id)
