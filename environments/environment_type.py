# environment_type.py
from typing import Any, Dict
from pydantic import BaseModel

class EnvironmentType(BaseModel):
    id: str
    name: str
    description: str
    environment: str
    env_params: Dict[str, Any] = {}
    min_players: int
    max_players: int