# File: agents/agent_logging.py
import json
import time
import numpy as np
from agents.agent_action import AgentAction

class AgentLogger:
    def __init__(self, agent_id: str):
        # set some standard attributes
        self.agent_id = agent_id
        self.log_filename = f"logs/{self.agent_id}.jsonl"
        self.time_initiated = time.strftime('%Y-%m-%d %H:%M:%S')

    def serialize_state(self, state: np.ndarray) -> list:
        """Convert numpy array state to a serializable list."""
        return state.tolist()

    def log_decision(self, game_id: str, step, state, thought_process: str, final_output: str, response: str, time_completed: str):
        # Check if the state needs serialization
        if isinstance(state, np.ndarray):
            state = self.serialize_state(state)

        # Convert AgentAction to string for JSON serialization
        if isinstance(final_output, AgentAction):
            final_output = final_output.name
        
        # check the response to see if it's agent action
        if isinstance(response, AgentAction):
            response = response.name
        
        # log the entry
        log_entry = {
            "agent_id": self.agent_id,
            "game_id": game_id,
            "time_initiated": self.time_initiated,
            "step": step,
            "state": state,
            "model_response": response,
            "agent_thinking": thought_process,
            "final_decision": final_output,
            "time_completed": time_completed
        }

        # Append to the log file
        with open(self.log_filename, 'a') as log_file:
            # Add the row
            log_file.write(json.dumps(log_entry) + '\n')

    def log_self_improvement_notes(self, game_id: str, step: int, self_improvement_notes: str):
        # log the self-improvement notes
        log_entry = {
            "agent_id": self.agent_id,
            "game_id": game_id,
            "step": step,
            "self_improvement_notes": self_improvement_notes,
            "time_logged": time.strftime('%Y-%m-%d %H:%M:%S')
        }

        # Append to the log file
        with open(self.log_filename, 'a') as log_file:
            # Add the row
            log_file.write(json.dumps(log_entry) + '\n')