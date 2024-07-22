# app/environments/environment_loader.py
import os
import json
import importlib
from typing import Any, List, Tuple

from environments.environment_type import EnvironmentType

class EnvironmentLoader:
    def __init__(self, config_path):
        # set the config path and load configs
        self.config_path = config_path
        self.env_configs = self.load_configs()

    def load_configs(self):
        # open and load the config
        with open(self.config_path) as f:
            return json.load(f)

    def get_environment_config(self, env_id):
        # loop through the config
        for env_config in self.env_configs:
            # check the environment id matches
            if env_config['id'] == env_id:
                # return the config
                return EnvironmentType(**env_config)
        raise ValueError(f"Environment with id '{env_id}' not found")

    def load_class(self, full_class_string):
        # get the module and class name
        module_path, class_name = full_class_string.rsplit('.', 1)

        # load the module
        module = importlib.import_module(module_path)

        # return
        return getattr(module, class_name)

    def get_environment(self, env_id) -> Tuple[Any, EnvironmentType]:
        # get the environment config
        env_config = self.get_environment_config(env_id)

        # get the environment class
        EnvClass = self.load_class(env_config.environment)

        # instantiate an instance of the environment
        env_instance = EnvClass(**env_config.env_params)

        # return the instance and the config
        return env_instance, env_config
    
    def list_environments(self) -> List[EnvironmentType]:
        return [self.get_environment_config(env_config['id']) for env_config in self.env_configs]


# Function to get the application root
def get_app_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create a global instance of EnvironmentLoader for ease of use
app_root = get_app_root()
environment_loader = EnvironmentLoader(os.path.join(app_root, 'config', 'environment_config.json'))

def get_environment(env_id) -> Tuple[Any, EnvironmentType]:
    # get the environment by id
    return environment_loader.get_environment(env_id)

def list_environments() -> List[EnvironmentType]:
    # list all available environments
    return environment_loader.list_environments()
