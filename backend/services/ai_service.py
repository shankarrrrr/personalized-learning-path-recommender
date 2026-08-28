import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, Any

# Load .env from the root HCL folder
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-3.6-flash')
        else:
            self.model = None

    def extract_profile(self, conversation_history: list) -> Dict[str, Any]:
        """Extracts goal, domain, level etc. from chat history."""
        if not self.model:
            # Fallback to mock logic
            return {
                "message": {"role": "assistant", "content": "I see! What's your current experience level?"},
                "profile": {
                    "goal": "Become a Data Analyst",
                    "domain": "Data Analytics",
                    "current_level": "Beginner",
                    "known_skills": [],
                    "interests": ["Python", "SQL"],
                    "time_budget": "3 months",
                    "preferred_format": "Video"
                },
                "is_complete": False
            }

        prompt = f"""
You are an AI learning path recommender assistant.
Based on the conversation history below, extract the learner's profile details.
Conversation History:
{json.dumps(conversation_history, indent=2)}

Also, based on what is missing from their profile (goal, domain, current_level, known_skills, time_budget), generate the NEXT question you should ask them. If you have enough to generate a path, say something encouraging and tell them you are generating their path.

Return the result STRICTLY as a JSON object with this exact structure:
{{
    "message": {{"role": "assistant", "content": "<your next question or response>"}},
    "profile": {{
        "goal": "...",
        "domain": "...",
        "current_level": "...",
        "known_skills": ["..."],
        "interests": ["..."],
        "time_budget": "...",
        "preferred_format": "..."
    }},
    "is_complete": true_or_false
}}
Set is_complete to true ONLY if you know their goal, domain, current_level, and time_budget.
"""
        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)

    def explain_recommendation(self, course_title: str, user_goal: str) -> str:
        """Generate a short 1-line rationale for why a course was recommended."""
        if not self.model:
            return f"Recommended because it builds the foundation for your goal to {user_goal}."
        
        prompt = f"In one short sentence, explain why a course titled '{course_title}' is recommended for someone whose goal is '{user_goal}'. Talk directly to the user (e.g. 'Recommended because you...')."
        response = self.model.generate_content(prompt)
        return response.text.strip()

ai_service = AIService()
