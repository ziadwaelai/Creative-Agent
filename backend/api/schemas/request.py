from pydantic import BaseModel, Field
from typing import List


class CreativeAgentRequest(BaseModel):
    """
    Request schema for creative content generation

    Represents input data for the creative agent to process
    Uses same fields as creative_agent_input dataclass for consistency
    """
    client_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name of the client/brand"
    )
    product_description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Detailed description of the product or service"
    )
    target_audience: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Description of the target audience"
    )
    tone_of_voice: List[str] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="List of desired tones (e.g., casual, formal, playful)"
    )
