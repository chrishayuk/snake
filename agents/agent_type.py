# File: app/agents/agent_type.py
from pydantic import BaseModel
from typing import Dict, Any, List

class AgentType(BaseModel):
    id: str
    name: str
    description: str
    agent: str
    agent_params: Dict[str, Any] = {}
    compatible_environments: List[str]
