# File: agents/treasure_hunt/treasure_hunt_agent.py
class TreasureHuntAction:
    class ActionType:
        GUESS = "GUESS"

    def __init__(self, action_type, row, col):
        self.action_type = action_type
        self.row = row
        self.col = col

    @classmethod
    def from_string(cls, action_str):
        parts = action_str.split()
        if len(parts) != 3:
            raise ValueError("Invalid action format")
        action_type, row, col = parts
        row = int(row)
        col = int(col)
        return cls(action_type, row, col)

    def __str__(self):
        return f"{self.action_type} {self.row} {self.col}"
