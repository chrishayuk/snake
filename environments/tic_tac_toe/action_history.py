# File: environments/tic_tac_toe/action_history.py
class ActionHistory:
    def __init__(self):
        # Initialize the history list
        self.history = []

    def add_record(self, step, player, action):
        """ Add a new record to the action history. """
        record = {
            'step': step,
            'player': player,  # Store the player ('X' or 'O')
            'action': action,  # Store the action (move number 1-9)
        }

        # add to the history
        self.history.append(record)

    def get_history(self):
        """Return the full action history."""
        return self.history

    def clear(self):
        """Clear the action history."""
        self.history = []
