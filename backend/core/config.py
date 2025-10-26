from dataclasses import dataclass
from typing import List


@dataclass
class creative_agent_input:
    """Legacy dataclass for input configuration"""
    client_name: str
    product_description: str
    target_audience: str
    tone_of_voice: List[str]
