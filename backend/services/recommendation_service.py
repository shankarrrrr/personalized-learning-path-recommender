import numpy as np
from services.embedding_service import embedding_service


class RecommendationService:
    """Vector-similarity course retrieval, optimized with batched numpy ops."""

    def __init__(self):
        pass

    def cosine_similarity(self, v1, v2):
        """Cosine similarity between two 1-D vectors (kept for API compat/tests)."""
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return float(dot_product / (norm_v1 * norm_v2))

    def _batched_cosine_similarity(self, query_vector: np.ndarray, matrix: np.ndarray) -> np.ndarray:
        """Cosine similarity between one query vector and each row of a matrix.

        Vectorized: a single matmul + broadcasted normalization instead of a
        Python loop over candidates. Returns a 1-D array of length len(matrix).
        """
        if matrix.size == 0:
            return np.array([])
        q = np.asarray(query_vector, dtype=np.float64)
        m = np.asarray(matrix, dtype=np.float64)
        q_norm = np.linalg.norm(q)
        m_norms = np.linalg.norm(m, axis=1)
        # Avoid division by zero.
        denom = m_norms * q_norm
        denom[denom == 0] = 1e-12
        return (m @ q) / denom

    def retrieve_best_course(self, skill_id: str, db_session, learner_profile, exclude_course_ids=None):
        """
        Retrieves the best matching course for a given skill based on semantic similarity
        and metadata filtering.
        exclude_course_ids: a list of course IDs to skip (e.g. if the user already skipped them)
        """
        if not embedding_service.is_initialized:
            embedding_service.build_course_index(db_session)

        goal = learner_profile.goal or "their career goal"
        level = learner_profile.current_level or "beginner"
        query_text = f"{skill_id} for an {level} learner preparing for {goal}"

        query_vector = embedding_service.get_embedding(query_text)

        # Use the cached course list instead of re-querying the DB on every skill
        # lookup — this eliminates N redundant SELECTs during a single path gen.
        all_courses = embedding_service.get_cached_courses(db_session)
        exclude_course_ids = exclude_course_ids or []

        # Filter for courses that teach the skill
        candidate_courses = [c for c in all_courses if skill_id in (c.skills_taught or []) and c.id not in exclude_course_ids]

        # Fallback if no specific course teaches this exact skill_id (or all were skipped)
        if not candidate_courses:
            candidate_courses = [c for c in all_courses if c.id not in exclude_course_ids]

        if not candidate_courses:
            return None  # Out of courses

        # Build the candidate matrix in one pass, keeping index alignment with
        # candidate_courses so we can map the argmax back to the Course object.
        vectors = []
        for course in candidate_courses:
            vec = embedding_service.course_index.get(course.id)
            if vec is not None:
                vectors.append(vec)
            else:
                vectors.append(np.zeros(embedding_service.embedding_dim))
        matrix = np.vstack(vectors) if vectors else np.array([])

        # Single vectorized similarity pass instead of a per-course Python loop.
        scores = self._batched_cosine_similarity(query_vector, matrix)

        # Metadata boosting (format match) applied after vectorized scoring.
        preferred = (learner_profile.preferred_format or "").lower()
        for i, course in enumerate(candidate_courses):
            if preferred and course.format and course.format.lower() == preferred:
                scores[i] += 0.05

        best_idx = int(np.argmax(scores))
        return candidate_courses[best_idx]


recommendation_service = RecommendationService()
