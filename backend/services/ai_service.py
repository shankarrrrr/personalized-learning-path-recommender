import os
from typing import Dict, Any
# from anthropic import Anthropic
# import openai

# This service handles LLM integrations. 
# We'll use mock responses if API keys are not set.

class AIService:
    def __init__(self):
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        # Initialize clients if keys exist

    def extract_profile(self, conversation_history: list) -> Dict[str, Any]:
        """Extracts goal, domain, level etc. from chat history."""
        # TODO: Implement real LLM call with structured output
        
        # Mock logic
        last_message = conversation_history[-1]['content'].lower()
        if "data analyst" in last_message or "data" in last_message:
            return {
                "goal": "Become a Data Analyst",
                "domain": "Data Analytics",
                "current_level": "Beginner",
                "known_skills": [],
                "interests": ["Python", "SQL"],
                "time_budget": "3 months",
                "preferred_format": "Video"
            }
        
        return None

    def explain_recommendation(self, course_title: str, user_goal: str) -> str:
        """Generate a short 1-line rationale for why a course was recommended."""
        # TODO: Implement LLM call
        return f"Recommended because it builds the foundation for your goal to {user_goal}."

ai_service = AIService()
