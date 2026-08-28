import numpy as np
from services.embedding_service import embedding_service

class RecommendationService:
    def __init__(self):
        pass

    def cosine_similarity(self, v1, v2):
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return float(dot_product / (norm_v1 * norm_v2))

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
        
        import models
        all_courses = db_session.query(models.Course).all()
        exclude_course_ids = exclude_course_ids or []
        
        # Filter for courses that teach the skill
        candidate_courses = [c for c in all_courses if skill_id in (c.skills_taught or []) and c.id not in exclude_course_ids]
        
        # Fallback if no specific course teaches this exact skill_id (or all were skipped)
        if not candidate_courses:
            candidate_courses = [c for c in all_courses if c.id not in exclude_course_ids]
            
        if not candidate_courses:
            return None # Out of courses

        best_course = None
        best_score = -2.0 # Cosine sim is between -1 and 1
        
        for course in candidate_courses:
            course_vector = embedding_service.course_index.get(course.id)
            if course_vector is not None:
                sim_score = self.cosine_similarity(query_vector, course_vector)
            else:
                sim_score = 0.0
            
            # Simple metadata boosting
            if learner_profile.preferred_format and learner_profile.preferred_format.lower() == course.format.lower():
                sim_score += 0.05
                
            if sim_score > best_score:
                best_score = sim_score
                best_course = course
                
        return best_course

recommendation_service = RecommendationService()
