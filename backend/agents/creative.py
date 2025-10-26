import logging
from typing import Dict, Any, Generator
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts.creative_prompts import (
    PRODUCT_ANALYSIS_PROMPT,
    AUDIENCE_ANALYSIS_PROMPT,
    CREATIVE_IDEATION_PROMPT,
    CONTENT_GENERATION_PROMPT,
    MARKETING_SUGGESTIONS_PROMPT,
    FINAL_CONTENT_PROMPT
)

logger = logging.getLogger(__name__)


class CreativeAgent:
    """
    Multi-step creative content generation agent

    Workflow:
    1. Analyze the product and extract key features
    2. Analyze the target audience and their needs
    3. Generate creative ideas based on product and audience
    4. Create compelling marketing content
    5. Suggest marketing tactics and channels
    6. Return final structured output as friendly KSA Arabic text with a funny tone
    """

    def __init__(self, model: str = "gpt-4-turbo", temperature: float = 0.7):
        """
        Initialize the Creative Agent

        Args:
            model: LLM model to use (default: gpt-4-turbo)
            temperature: Creativity level 0-1 (default: 0.7)
        """
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.llm_streaming = ChatOpenAI(model=model, temperature=temperature, streaming=True)

    def _stream_text(self, prompt_template: str, input_vars: Dict[str, Any]) -> Generator[str, None, None]:
        """
        Stream text output from LLM token by token

        Args:
            prompt_template: The prompt template to use
            input_vars: Variables to fill in the template

        Yields:
            Text chunks as they're generated
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm_streaming

        try:
            for chunk in chain.stream(input_vars):
                if hasattr(chunk, 'content'):
                    yield chunk.content
                else:
                    yield str(chunk)
        except Exception as e:
            logger.error(f"Error in streaming: {str(e)}")
            raise

    def run_full_pipeline_streaming(
        self,
        client_name: str,
        product_description: str,
        target_audience: str,
        tone_of_voice: list
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Run the complete multi-step creative generation pipeline with streaming output

        Each step streams its output token by token like ChatGPT

        Args:
            client_name: Name of the client/brand
            product_description: Detailed product description
            target_audience: Description of target audience
            tone_of_voice: List of desired tones

        Yields:
            Events with streaming content for each step
        """
        logger.info(f"Starting streaming creative agent pipeline for {client_name}")

        try:
            # Step 1: Analyze Product (with streaming)
            logger.info("Step 1: Streaming product analysis")
            yield {"type": "step_start", "step": 1, "title": "تحليل المنتج"}

            product_analysis_parts = []
            for chunk in self._stream_text(PRODUCT_ANALYSIS_PROMPT, {
                "client_name": client_name,
                "product_description": product_description
            }):
                product_analysis_parts.append(chunk)
                yield {"type": "step_stream", "step": 1, "content": chunk}

            product_analysis = "".join(product_analysis_parts)
            yield {"type": "step_complete", "step": 1, "data": product_analysis}

            # Step 2: Analyze Audience (with streaming)
            logger.info("Step 2: Streaming audience analysis")
            yield {"type": "step_start", "step": 2, "title": "تحليل الجمهور"}

            audience_analysis_parts = []
            tone_str = ", ".join(tone_of_voice)
            for chunk in self._stream_text(AUDIENCE_ANALYSIS_PROMPT, {
                "target_audience": target_audience,
                "tone_of_voice": tone_str
            }):
                audience_analysis_parts.append(chunk)
                yield {"type": "step_stream", "step": 2, "content": chunk}

            audience_analysis = "".join(audience_analysis_parts)
            yield {"type": "step_complete", "step": 2, "data": audience_analysis}

            # Step 3: Generate Ideas (with streaming)
            logger.info("Step 3: Streaming creative ideas")
            yield {"type": "step_start", "step": 3, "title": "توليد الأفكار"}

            creative_ideas_parts = []
            for chunk in self._stream_text(CREATIVE_IDEATION_PROMPT, {
                "product_analysis": product_analysis,
                "audience_analysis": audience_analysis,
                "tone_of_voice": tone_str
            }):
                creative_ideas_parts.append(chunk)
                yield {"type": "step_stream", "step": 3, "content": chunk}

            creative_ideas = "".join(creative_ideas_parts)
            yield {"type": "step_complete", "step": 3, "data": creative_ideas}

            # Step 4: Generate Content (with streaming)
            logger.info("Step 4: Streaming content generation")
            yield {"type": "step_start", "step": 4, "title": "توليد المحتوى"}

            generated_content_parts = []
            for chunk in self._stream_text(CONTENT_GENERATION_PROMPT, {
                "product_analysis": product_analysis,
                "audience_analysis": audience_analysis,
                "creative_ideas": creative_ideas,
                "tone_of_voice": tone_str
            }):
                generated_content_parts.append(chunk)
                yield {"type": "step_stream", "step": 4, "content": chunk}

            generated_content = "".join(generated_content_parts)
            yield {"type": "step_complete", "step": 4, "data": generated_content}

            # Step 5: Marketing Suggestions (with streaming)
            logger.info("Step 5: Streaming marketing suggestions")
            yield {"type": "step_start", "step": 5, "title": "الاقتراحات التسويقية"}

            marketing_suggestions_parts = []
            for chunk in self._stream_text(MARKETING_SUGGESTIONS_PROMPT, {
                "generated_content": generated_content,
                "target_audience": target_audience,
                "tone_of_voice": tone_str
            }):
                marketing_suggestions_parts.append(chunk)
                yield {"type": "step_stream", "step": 5, "content": chunk}

            marketing_suggestions = "".join(marketing_suggestions_parts)
            yield {"type": "step_complete", "step": 5, "data": marketing_suggestions}

            # Step 6: Final Output (with streaming)
            logger.info("Step 6: Streaming final output")
            yield {"type": "step_start", "step": 6, "title": "الصياغة النهائية"}

            final_message_parts = []
            for chunk in self._stream_text(FINAL_CONTENT_PROMPT, {
                "product_analysis": product_analysis,
                "audience_analysis": audience_analysis,
                "creative_ideas": creative_ideas,
                "generated_content": generated_content,
                "marketing_suggestions": marketing_suggestions,
                "tone_of_voice": tone_str
            }):
                final_message_parts.append(chunk)
                yield {"type": "step_stream", "step": 6, "content": chunk}

            final_message = "".join(final_message_parts)
            yield {"type": "step_complete", "step": 6, "data": final_message}

            # Final completion event
            yield {"type": "complete", "final_content": final_message}
            logger.info(f"Pipeline completed successfully for {client_name}")

        except Exception as e:
            logger.error(f"Error in streaming creative agent pipeline: {str(e)}")
            yield {"type": "error", "message": str(e)}
            raise
