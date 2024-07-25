class ActionHistory:
    def __init__(self):
        self.history = []

    def add_record(self, step, snake_head_position, snake_direction, snake_length, action):
        record = {
            "step": step,
            "snake_head_position": snake_head_position,
            "snake_direction": snake_direction,
            "snake_length": snake_length,
            "action": action
        }
        self.history.append(record)

    def get_history(self):
        return self.history
