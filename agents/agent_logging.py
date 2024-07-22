# File: app/utils/logging_utility.py
import json
import time

class Logger:
    def __init__(self, agent_id: str):
        # set some standard attributes
        self.agent_id = agent_id
        self.log_filename = f"logs/{self.agent_id}.jsonl"
        self.time_initiated = time.strftime('%Y-%m-%d %H:%M:%S')

    def log_decision(self, game_id:str, state: str, thought_process: str, final_output: str, response: str, time_completed: str):
        log_entry = {
            "agent_id": self.agent_id,
            "game_id": game_id,
            "time_initiated": self.time_initiated,
            "state": state,
            "model_response": response,
            "agent_thinking": thought_process,
            "final_decision": final_output,
            "time_completed": time_completed
        }

        # append to the log gile
        with open(self.log_filename, 'a') as log_file:
            # add the row
            log_file.write(json.dumps(log_entry) + '\n')
