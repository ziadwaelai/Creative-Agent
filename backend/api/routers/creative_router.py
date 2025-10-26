"""
Creative Agent API Routes
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from api.schemas.request import CreativeAgentRequest
from api.schemas.response import CreativeAgentResponse
from agents.creative import CreativeAgent
import logging
import os
from dotenv import load_dotenv
import json
import asyncio

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize the creative agent with valid model
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
creative_agent = CreativeAgent(model=MODEL, temperature=TEMPERATURE)


@router.post(
    "/generate-creative-content-stream",
    status_code=status.HTTP_200_OK,
    summary="Generate creative content with streaming progress",
    description="""
    Generate creative marketing content with real-time streaming of each step.
    Returns Server-Sent Events (SSE) stream showing progress of each pipeline step.
    """
)
async def create_creative_content_stream(request: CreativeAgentRequest):
    """
    Generate creative marketing content with streaming progress updates.

    Streams real-time updates for each step of the pipeline:
    - Step 1: Product Analysis
    - Step 2: Audience Analysis
    - Step 3: Creative Ideas
    - Step 4: Content Generation
    - Step 5: Marketing Suggestions
    - Step 6: Final Output Formatting
    """
    def event_generator():
        try:
            logger.info(f"Starting streaming pipeline for: {request.client_name}")

            # Validate input
            if not request.tone_of_voice:
                yield f"data: {json.dumps({'type': 'error', 'message': 'At least one tone of voice is required'})}\n\n"
                return

            # Use the new streaming pipeline
            for event in creative_agent.run_full_pipeline_streaming(
                client_name=request.client_name,
                product_description=request.product_description,
                target_audience=request.target_audience,
                tone_of_voice=request.tone_of_voice
            ):
                # Send each event as SSE
                yield f"data: {json.dumps(event)}\n\n"

            logger.info(f"Successfully completed streaming for: {request.client_name}")

        except ValueError as ve:
            logger.error(f"Validation error: {str(ve)}")
            yield f"data: {json.dumps({'type': 'error', 'message': f'خطأ في التحقق: {str(ve)}'})}\n\n"
        except Exception as e:
            logger.error(f"Error in streaming pipeline: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'message': f'خطأ: {str(e)}'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )
