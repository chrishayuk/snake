# File: agents/agent_config.py
from pydantic import BaseModel
from typing import Dict, Any, List

class AgentConfig(BaseModel):
    id: str
    name: str
    type: str
    description: str
    agent: str
    agent_type: str
    agent_params: Dict[str, Any] = {}
    compatible_environments: List[str]
