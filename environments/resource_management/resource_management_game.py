import json
import random

class ResourceManagementGame:
    def __init__(self, config_file):
        self.load_game(config_file)

    def load_game(self, config_file):
        with open(config_file, 'r') as file:
            self.config = json.load(file)
        
        self.resources = {resource['name']: resource['initial_amount'] for resource in self.config['resources']}
        self.events = self.config['events']
        self.goals = self.config['goals']

    def display_status(self):
        print(f"┌{'─' * 57}┐")
        print(f"│ {self.config['game']['name']:^55} │")
        print(f"└{'─' * 57}┘")
        print("│ Resources:                                              │")
        print(f"│ {'─' * 55} │")
        for resource, amount in self.resources.items():
            print(f"│ {resource:<20}: {amount:<30} │")
        print(f"│ {'─' * 55} │")
        print("│ Actions:                                                │")
        for i, action in enumerate(self.config['actions']):
            print(f"│ {i + 1}. {action['name']}                                      │")
            for j, option in enumerate(action['options']):
                changes = option.get('resource_changes', {})
                changes_str = ', '.join(f'{k}: {v:+}' for k, v in changes.items())
                print(f"│    {chr(97 + j)}) {option['name']} ({changes_str}) │")
        print(f"│ {'─' * 55} │")
        print("│ Current Events:                                         │")
        for event in self.events:
            print(f"│ {event['name']:<55}│")
        print(f"│ {'─' * 55} │")
        print("│ Goals:                                                  │")
        print("│ Short-term:                                             │")
        for goal in self.goals["short_term"]:
            print(f"│ {goal:<55}│")
        print("│ Long-term:                                              │")
        for goal in self.goals["long_term"]:
            print(f"│ {goal:<55}│")
        print("└─────────────────────────────────────────────────────────┘")
        print("│ > Your choice:                                          │")
        print("└─────────────────────────────────────────────────────────┘")

    def update_resources(self, changes):
        for resource, change in changes.items():
            self.resources[resource] += change

    def trigger_event(self):
        event = random.choice(self.events)
        print(f"Event: {event['name']}")
        self.update_resources(event["effects"])

    def play(self):
        while True:
            self.display_status()
            choice = input("Enter your choice (e.g., 1a): ").strip().lower()

            try:
                action_index = int(choice[0]) - 1
                option_index = ord(choice[1]) - ord('a')
                action = self.config['actions'][action_index]
                option = action['options'][option_index]
                self.update_resources(option.get('resource_changes', {}))
            except (IndexError, ValueError):
                print("Invalid choice, please try again.")
                continue

            # Trigger a random event occasionally
            if random.random() < 0.3:  # 30% chance of an event occurring each turn
                self.trigger_event()

# To run the game with a specified JSON file:
game = ResourceManagementGame('configurations/podcast_management.json')
game.play()
