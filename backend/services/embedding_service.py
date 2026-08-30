import os
import numpy as np
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load .env from the root HCL folder
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

# Embedding model + dimensionality (new google-genai SDK).
# gemini-embedding-2 produces 3072-dimensional vectors.
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-2")
EMBEDDING_DIM = int(os.getenv("GEMINI_EMBEDDING_DIM", "3072"))


class EmbeddingService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Expose config as instance attributes for easy introspection/override.
        self.embedding_model = EMBEDDING_MODEL
        self.embedding_dim = EMBEDDING_DIM
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
        
        # In-memory vector store mapping: course_id -> numpy vector
        self.course_index = {} 
        self.is_initialized = False
        # Simple in-memory cache to avoid re-embedding identical query strings.
        self._query_cache = {}
        
    def get_embedding(self, text: str) -> list:
        """Generate an embedding for the given text using Gemini."""
        if not self.client:
            # Fallback mock embedding (zero vector of the configured dimension)
            return [0.0] * self.embedding_dim

        # Return cached embedding if we already embedded this exact text.
        if text in self._query_cache:
            return self._query_cache[text]

        response = self.client.models.embed_content(
            model=self.embedding_model,
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
        )
        embedding = response.embeddings[0].values
        self._query_cache[text] = embedding
        return embedding
        
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
