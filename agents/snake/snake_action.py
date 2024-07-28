# File: agents/snake/snake_action.py
from agents.agent_action import AgentAction

class SnakeAction(AgentAction):
    # actions
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def __init__(self, action):
        # check for a valid action
        if action not in {self.NONE, self.UP, self.RIGHT, self.DOWN, self.LEFT}:
            # invalid action
            raise ValueError(f"Invalid action: {action}")
        
        # set the action
        self.action = action

    def __str__(self):
        # convert to a string
        return {self.NONE: "NONE", self.UP: "UP", self.RIGHT: "RIGHT", self.DOWN: "DOWN", self.LEFT: "LEFT"}[self.action]

    @classmethod
    def from_string(cls, action_str):
        # setup the mapping
        mapping = {"NONE": cls.NONE, "UP": cls.UP, "RIGHT": cls.RIGHT, "DOWN": cls.DOWN, "LEFT": cls.LEFT}

        # ensure action is within mapping
        if action_str not in mapping:
            # invalid mapping
            raise ValueError(f"Invalid action string: {action_str}")
        
        # return the mapping
        return cls(mapping[action_str])
