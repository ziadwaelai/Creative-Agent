from pydantic import BaseModel, Field


class CreativeAgentResponse(BaseModel):
    """
    Response schema for creative content generation

    Contains the final generated creative content message in KSA local tone
    This is the only output from the complete pipeline
    """
    final_content: str = Field(
        ...,
        description="The final generated creative content message in KSA friendly tone"
    )


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str = Field(description="Error message")
    status_code: int = Field(description="HTTP status code")
