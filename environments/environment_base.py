# environment_base.py
from abc import ABC, abstractmethod

class Environment(ABC):
    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def step(self, action):
        pass

    @abstractmethod
    def get_render(self):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def reset(self):
        pass