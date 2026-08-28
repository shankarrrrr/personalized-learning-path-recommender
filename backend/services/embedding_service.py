import os
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env from the root HCL folder
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

class EmbeddingService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        # In-memory vector store mapping: course_id -> numpy vector
        self.course_index = {} 
        self.is_initialized = False
        
    def get_embedding(self, text: str) -> list:
        if not self.api_key:
            # Fallback mock embedding
            return [0.0] * 768
            
        result = genai.embed_content(
            model="models/gemini-embedding-2",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
        
    def build_course_index(self, db_session):
        """Loads all courses from the DB and caches their vectors."""
        # Local import to avoid circular dependency
        import models
        courses = db_session.query(models.Course).all()
        count = 0
        for course in courses:
            if course.embedding_vector:
                # Convert the JSON list to a fast numpy array
                self.course_index[course.id] = np.array(course.embedding_vector)
                count += 1
        self.is_initialized = True
        print(f"Loaded {count} course vectors into memory.")

embedding_service = EmbeddingService()
