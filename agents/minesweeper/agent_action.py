# File: agent_action.py
from enum import Enum

class MinesweeperAction:
    class ActionType(Enum):
        REVEAL = 'reveal'
        FLAG = 'flag'

    def __init__(self, action_type, row, col):
        self.action_type = action_type
        self.row = row
        self.col = col

    def __str__(self):
        return f"{self.action_type.value} {self.row} {self.col}"

    @classmethod
    def from_string(cls, action_string):
        parts = action_string.split()
        if len(parts) != 3:
            raise ValueError("Invalid action string format")
        
        action_type = parts[0].lower()
        if action_type == 'reveal':
            action_type = cls.ActionType.REVEAL
        elif action_type == 'flag':
            action_type = cls.ActionType.FLAG
        else:
            raise ValueError(f"Invalid action type: {action_type}")
        
        row = int(parts[1])
        col = int(parts[2])
        
        return cls(action_type, row, col)