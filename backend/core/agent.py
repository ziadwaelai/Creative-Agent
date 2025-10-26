import json
import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from backend.prompts.creative_prompts import (
    PRODUCT_ANALYSIS_PROMPT,
    AUDIENCE_ANALYSIS_PROMPT,
    CREATIVE_IDEATION_PROMPT,
    CONTENT_GENERATION_PROMPT,
    MARKETING_SUGGESTIONS_PROMPT,
    FULL_PIPELINE_PROMPT
)

logger = logging.getLogger(__name__)


class CreativeAgent:
    """
    Multi-step creative content generation agent

    Workflow (6 Steps):
    1. Analyze the product and extract key features
    2. Analyze the target audience and their needs
    3. Generate creative ideas based on product and audience
    4. Create compelling marketing content
    5. Suggest marketing tactics and channels
    6. (Optional) Generate comprehensive final report with KSA cultural insights
    """

    def __init__(self, model: str = "gpt-4", temperature: float = 0.7):
        """
        Initialize the Creative Agent

        Args:
            model: LLM model to use (default: gpt-4)
            temperature: Creativity level 0-1 (default: 0.7)
        """
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.json_parser = JsonOutputParser()

    def step_1_analyze_product(self, client_name: str, product_description: str) -> Dict[str, Any]:
        """
        Step 1: Analyze product and extract key information

        Args:
            client_name: Name of the client/brand
            product_description: Detailed product description

        Returns:
            Dictionary with product analysis
        """
        logger.info(f"Step 1: Analyzing product for {client_name}")

        prompt = ChatPromptTemplate.from_template(PRODUCT_ANALYSIS_PROMPT)

        chain = prompt | self.llm | self.json_parser

        try:
            result = chain.invoke({
                "client_name": client_name,
                "product_description": product_description
            })
            logger.info("Step 1 completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in Step 1: {str(e)}")
            # Fallback response
            return {
                "product_name": client_name,
                "key_features": ["مميز", "جودة عالية", "موثوق"],
                "unique_selling_point": "منتج فريد وخاص",
                "product_category": "منتج"
            }

    def step_2_analyze_audience(self, target_audience: str, tone_of_voice: list) -> Dict[str, Any]:
        """
        Step 2: Analyze target audience and communication style

        Args:
            target_audience: Description of target audience
            tone_of_voice: List of desired tones

        Returns:
            Dictionary with audience analysis
        """
        logger.info("Step 2: Analyzing target audience")

        prompt = ChatPromptTemplate.from_template(AUDIENCE_ANALYSIS_PROMPT)

        chain = prompt | self.llm | self.json_parser

        tone_str = ", ".join(tone_of_voice)

        try:
            result = chain.invoke({
                "target_audience": target_audience,
                "tone_of_voice": tone_str
            })
            logger.info("Step 2 completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in Step 2: {str(e)}")
            # Fallback response
            return {
                "demographic": target_audience,
                "psychographic": "بحث عن جودة وموثوقية",
                "pain_points": ["البحث عن خيارات جيدة", "عدم الثقة"],
                "desires": ["جودة عالية", "سعر عادل", "خدمة جيدة"],
                "communication_style": tone_str
            }

    def step_3_generate_ideas(
        self,
        product_analysis: Dict[str, Any],
        audience_analysis: Dict[str, Any],
        tone_of_voice: list
    ) -> Dict[str, Any]:
        """
        Step 3: Generate creative ideas based on product and audience analysis

        Args:
            product_analysis: Output from Step 1
            audience_analysis: Output from Step 2
            tone_of_voice: List of desired tones

        Returns:
            Dictionary with creative ideas
        """
        logger.info("Step 3: Generating creative ideas")

        prompt = ChatPromptTemplate.from_template(CREATIVE_IDEATION_PROMPT)

        chain = prompt | self.llm | self.json_parser

        tone_str = ", ".join(tone_of_voice)

        try:
            result = chain.invoke({
                "product_analysis": json.dumps(product_analysis, ensure_ascii=False),
                "audience_analysis": json.dumps(audience_analysis, ensure_ascii=False),
                "tone_of_voice": tone_str
            })
            logger.info("Step 3 completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in Step 3: {str(e)}")
            # Fallback response
            return {
                "creative_ideas": [
                    {
                        "idea_title": "الفكرة الأولى",
                        "concept": "ركز على الجودة والموثوقية",
                        "angle": "الثقة والاعتمادية"
                    },
                    {
                        "idea_title": "الفكرة الثانية",
                        "concept": "ركز على الفائدة والقيمة",
                        "angle": "القيمة المضافة"
                    },
                    {
                        "idea_title": "الفكرة الثالثة",
                        "concept": "ركز على الاتصال العاطفي",
                        "angle": "الاتصال العاطفي"
                    }
                ]
            }

    def step_4_generate_content(
        self,
        product_analysis: Dict[str, Any],
        audience_analysis: Dict[str, Any],
        creative_ideas: Dict[str, Any],
        tone_of_voice: list
    ) -> Dict[str, Any]:
        """
        Step 4: Generate compelling marketing content

        Args:
            product_analysis: Output from Step 1
            audience_analysis: Output from Step 2
            creative_ideas: Output from Step 3
            tone_of_voice: List of desired tones

        Returns:
            Dictionary with generated content
        """
        logger.info("Step 4: Generating marketing content")

        prompt = ChatPromptTemplate.from_template(CONTENT_GENERATION_PROMPT)

        chain = prompt | self.llm | self.json_parser

        tone_str = ", ".join(tone_of_voice)

        try:
            result = chain.invoke({
                "product_analysis": json.dumps(product_analysis, ensure_ascii=False),
                "audience_analysis": json.dumps(audience_analysis, ensure_ascii=False),
                "creative_ideas": json.dumps(creative_ideas, ensure_ascii=False),
                "tone_of_voice": tone_str
            })
            logger.info("Step 4 completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in Step 4: {str(e)}")
            # Fallback response
            return {
                "generated_content": "محتوى تسويقي إبداعي يجمع بين الجودة والموثوقية",
                "creative_angle_used": "التركيز على القيمة والثقة",
                "key_messages": ["جودة عالية", "موثوق", "مناسب لاحتياجاتك"]
            }

    def step_5_marketing_suggestions(
        self,
        generated_content: Dict[str, Any],
        target_audience: str,
        tone_of_voice: list
    ) -> Dict[str, Any]:
        """
        Step 5: Generate marketing suggestions and tactics

        Args:
            generated_content: Output from Step 4
            target_audience: Description of target audience
            tone_of_voice: List of desired tones

        Returns:
            Dictionary with marketing suggestions
        """
        logger.info("Step 5: Generating marketing suggestions")

        prompt = ChatPromptTemplate.from_template(MARKETING_SUGGESTIONS_PROMPT)

        chain = prompt | self.llm | self.json_parser

        tone_str = ", ".join(tone_of_voice)

        try:
            result = chain.invoke({
                "generated_content": json.dumps(generated_content, ensure_ascii=False),
                "target_audience": target_audience,
                "tone_of_voice": tone_str
            })
            logger.info("Step 5 completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in Step 5: {str(e)}")
            # Fallback response
            return {
                "marketing_suggestions": [
                    {
                        "channel": "وسائل التواصل الاجتماعي",
                        "tactic": "نشر محتوى يومي وجذاب",
                        "timing": "في أوقات الذروة"
                    },
                    {
                        "channel": "البريد الإلكتروني",
                        "tactic": "إرسال رسائل إخبارية منتظمة",
                        "timing": "مرة أسبوعية"
                    },
                    {
                        "channel": "التعاون مع المؤثرين",
                        "tactic": "التعاون مع مؤثرين متخصصين",
                        "timing": "حملات موسمية"
                    }
                ]
            }

    def step_6_full_pipeline_report(
        self,
        product_analysis: Dict[str, Any],
        audience_analysis: Dict[str, Any],
        creative_ideas: Dict[str, Any],
        generated_content: Dict[str, Any],
        marketing_suggestions: Dict[str, Any],
        target_audience: str,
        tone_of_voice: list
    ) -> Dict[str, Any]:
        """
        Step 6 (Optional): Generate comprehensive final report with KSA cultural insights

        Combines all previous steps and produces a comprehensive executive summary
        tailored to the Saudi Arabian market

        Args:
            product_analysis: Output from Step 1
            audience_analysis: Output from Step 2
            creative_ideas: Output from Step 3
            generated_content: Output from Step 4
            marketing_suggestions: Output from Step 5
            target_audience: Description of target audience
            tone_of_voice: List of desired tones

        Returns:
            Dictionary with comprehensive final report
        """
        logger.info("Step 6: Generating comprehensive final report")

        prompt = ChatPromptTemplate.from_template(FULL_PIPELINE_PROMPT)

        chain = prompt | self.llm | self.json_parser

        tone_str = ", ".join(tone_of_voice)

        try:
            result = chain.invoke({
                "product_analysis": json.dumps(product_analysis, ensure_ascii=False),
                "audience_analysis": json.dumps(audience_analysis, ensure_ascii=False),
                "creative_ideas": json.dumps(creative_ideas, ensure_ascii=False),
                "generated_content": json.dumps(generated_content, ensure_ascii=False),
                "marketing_suggestions": json.dumps(marketing_suggestions, ensure_ascii=False),
                "target_audience": target_audience,
                "tone_of_voice": tone_str
            })
            logger.info("Step 6 completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in Step 6: {str(e)}")
            # Fallback response
            return {
                "executive_summary": "ملخص شامل يجمع كل المراحل السابقة",
                "saudified_messaging": "الرسائل المصاغة بما يناسب السوق السعودي",
                "cultural_insights": ["فهم عميق للسوق السعودي", "احترام القيم الثقافية", "التكيف مع التوقعات المحلية"],
                "implementation_roadmap": [
                    {
                        "phase": "إطلاق",
                        "actions": ["تحضير المحتوى", "إعداد الحملات"],
                        "timeline": "أسبوعان"
                    }
                ],
                "success_metrics": ["زيادة التوعية", "تحسين المشاركة", "زيادة المبيعات"],
                "final_recommendations": "توصيات شاملة للتنفيذ الناجح"
            }

    def run_full_pipeline(
        self,
        client_name: str,
        product_description: str,
        target_audience: str,
        tone_of_voice: list,
        include_executive_report: bool = False
    ) -> Dict[str, Any]:
        """
        Run the complete multi-step creative generation pipeline

        Args:
            client_name: Name of the client/brand
            product_description: Detailed product description
            target_audience: Description of target audience
            tone_of_voice: List of desired tones
            include_executive_report: If True, includes Step 6 comprehensive report (default: False)

        Returns:
            Final result with generated content and suggestions
        """
        logger.info(f"Starting creative agent pipeline for {client_name}")

        try:
            # Step 1: Analyze Product
            product_analysis = self.step_1_analyze_product(client_name, product_description)

            # Step 2: Analyze Audience
            audience_analysis = self.step_2_analyze_audience(target_audience, tone_of_voice)

            # Step 3: Generate Ideas
            creative_ideas = self.step_3_generate_ideas(
                product_analysis,
                audience_analysis,
                tone_of_voice
            )

            # Step 4: Generate Content
            generated_content = self.step_4_generate_content(
                product_analysis,
                audience_analysis,
                creative_ideas,
                tone_of_voice
            )

            # Step 5: Marketing Suggestions
            marketing_suggestions = self.step_5_marketing_suggestions(
                generated_content,
                target_audience,
                tone_of_voice
            )

            # Format final response
            suggestions_list = [
                f"{s['tactic']} ({s['channel']})"
                for s in marketing_suggestions.get("marketing_suggestions", [])
            ]

            final_result = {
                "client_name": client_name,
                "generated_content": generated_content.get("generated_content", ""),
                "creative_angle": generated_content.get("creative_angle_used", ""),
                "marketing_suggestions": suggestions_list,
                "key_messages": generated_content.get("key_messages", [])
            }

            # Step 6 (Optional): Generate comprehensive report
            if include_executive_report:
                logger.info("Generating executive report...")
                executive_report = self.step_6_full_pipeline_report(
                    product_analysis,
                    audience_analysis,
                    creative_ideas,
                    generated_content,
                    marketing_suggestions,
                    target_audience,
                    tone_of_voice
                )
                final_result["executive_report"] = executive_report

            logger.info(f"Pipeline completed successfully for {client_name}")
            return final_result

        except Exception as e:
            logger.error(f"Error in creative agent pipeline: {str(e)}")
            raise
