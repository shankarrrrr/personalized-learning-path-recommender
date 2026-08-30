import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import Dict, Any, List
import models
import database
from sqlalchemy.orm import Session

# Load .env from the root HCL folder
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

# Model identifiers (new google-genai SDK).
# gemini-3.6-flash is the current non-deprecated chat model.
TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL", "gemini-3.6-flash")


class AIService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Expose the model id as an instance attribute for easy introspection/override.
        self.text_model = TEXT_MODEL
        if self.api_key:
            # New official SDK: a Client is configured with the API key once,
            # then used for all model calls (no global genai.configure() needed).
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def get_career_recommendations(self, user_interests: List[str], user_background: str = "") -> List[Dict[str, Any]]:
        """Get career path recommendations based on user interests and background."""
        try:
            # Get all career paths from database
            db = database.SessionLocal()
            all_careers = db.query(models.CareerPath).all()
            db.close()
            
            if not all_careers:
                return []
            
            # Create a prompt to get AI recommendations
            careers_summary = []
            for career in all_careers:
                careers_summary.append({
                    "id": career.id,
                    "title": career.title,
                    "domain": career.domain,
                    "description": career.description[:150] + "...",
                    "difficulty": career.difficulty_level,
                    "time_months": career.estimated_time_months,
                    "salary_range": f"${career.avg_salary_min//1000}k-${career.avg_salary_max//1000}k" if career.avg_salary_min else "N/A"
                })
            
            prompt = f"""
Based on the user's interests and background, recommend the top 3 most suitable career paths from the available options.

User Interests: {', '.join(user_interests) if user_interests else 'Not specified'}
User Background: {user_background or 'Not specified'}

Available Career Paths:
{json.dumps(careers_summary, indent=2)}

Please return ONLY a JSON array with the top 3 career recommendations in this exact format:
[
  {{
    "career_id": "career_id_here",
    "title": "Career Title",
    "match_reason": "Brief explanation of why this matches the user's interests",
    "confidence": 0.85
  }}
]

Sort by best match (highest confidence) first.
"""
            
            if not self.client:
                # Fallback recommendations if no API key
                return [
                    {
                        "career_id": "data_scientist",
                        "title": "Data Scientist", 
                        "match_reason": "Great starting point for tech careers",
                        "confidence": 0.8
                    },
                    {
                        "career_id": "full_stack_web_developer",
                        "title": "Full Stack Web Developer",
                        "match_reason": "Versatile and in-demand role",
                        "confidence": 0.7
                    }
                ]

            response = self.client.models.generate_content(
                model=self.text_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
            )

            recommendations = json.loads(response.text)
            return recommendations[:3]  # Ensure max 3 recommendations
            
        except Exception as e:
            print(f"Error getting career recommendations: {e}")
            # Return fallback recommendations
            return [
                {
                    "career_id": "data_scientist", 
                    "title": "Data Scientist",
                    "match_reason": "Popular and well-paying tech career",
                    "confidence": 0.7
                }
            ]
    def extract_profile(self, conversation_history: list) -> Dict[str, Any]:
        """Extracts goal, domain, level etc. from chat history and suggests career paths."""
        if not self.client:
            # Fallback to mock logic with career suggestions
            return {
                "message": {"role": "assistant", "content": "I see you're interested in tech! Based on what you've shared, here are some career paths that might interest you: Data Scientist, Web Developer, or DevOps Engineer. Which of these sounds most appealing, or would you like to explore other options?"},
                "profile": {
                    "goal": "Become a Data Analyst",
                    "domain": "Data Analytics", 
                    "current_level": "Beginner",
                    "known_skills": [],
                    "interests": ["Python", "SQL"],
                    "time_budget": "3 months",
                    "preferred_format": "Video"
                },
                "career_suggestions": [
                    {"career_id": "data_scientist", "title": "Data Scientist", "match_reason": "Matches your analytical interests", "confidence": 0.8}
                ],
                "is_complete": False
            }

        # Extract user interests and background from conversation
        user_interests = []
        user_background = ""
        
        for message in conversation_history:
            if message.get("role") == "user":
                content = message.get("content", "").lower()
                # Simple keyword extraction for interests
                tech_keywords = ["programming", "coding", "web", "mobile", "data", "ai", "machine learning", 
                               "design", "security", "cloud", "blockchain", "python", "javascript", "react"]
                user_interests.extend([word for word in tech_keywords if word in content])
                user_background += content + " "
        
        # Remove duplicates
        user_interests = list(set(user_interests))

        prompt = f"""
You are an AI learning path recommender assistant helping users discover their ideal tech career.
Based on the conversation history below, extract the learner's profile details.

Conversation History:
{json.dumps(conversation_history, indent=2)}

Your response should be encouraging and help guide them towards a suitable career path.
If they haven't specified a clear goal yet, suggest exploring career options based on their interests.

If they mention interests like:
- "data", "analytics", "statistics" → suggest Data Science careers
- "websites", "web", "frontend", "backend" → suggest Web Development 
- "mobile", "apps", "ios", "android" → suggest Mobile Development
- "security", "hacking", "cybersecurity" → suggest Cybersecurity
- "cloud", "servers", "infrastructure" → suggest DevOps/Cloud
- "design", "ui", "ux", "visual" → suggest UI/UX Design
- "ai", "machine learning", "ml" → suggest ML Engineering

Return the result STRICTLY as a JSON object with this exact structure:
{{
    "message": {{"role": "assistant", "content": "<your encouraging response with career suggestions>"}},
    "profile": {{
        "goal": "...",
        "domain": "...", 
        "current_level": "...",
        "known_skills": ["..."],
        "interests": ["..."],
        "time_budget": "...",
        "preferred_format": "..."
    }},
    "suggested_careers": [
        {{"career_id": "suggested_career_id", "title": "Career Title", "reason": "why this fits"}}
    ],
    "is_complete": true_or_false
}}

Set is_complete to true ONLY if you have their goal, domain, current_level, and time_budget.
Include 1-3 career suggestions in suggested_careers based on their interests.
"""
        
        response = self.client.models.generate_content(
            model=self.text_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        result = json.loads(response.text)
        
        # If we have user interests, get AI-powered career recommendations
        if user_interests and "suggested_careers" not in result:
            career_recs = self.get_career_recommendations(user_interests, user_background)
            result["career_suggestions"] = career_recs
        
        return result

    def explain_recommendation(self, course_title: str, user_goal: str) -> str:
        """Generate a short 1-line rationale for why a course was recommended."""
        if not self.client:
            return f"Recommended because it builds the foundation for your goal to {user_goal}."
        
        prompt = f"In one short sentence, explain why a course titled '{course_title}' is recommended for someone whose goal is '{user_goal}'. Talk directly to the user (e.g. 'Recommended because you...')."
        response = self.client.models.generate_content(model=self.text_model, contents=prompt)
        return response.text.strip()

ai_service = AIService()
