import os
from sqlalchemy.orm import Session
import database, models
from services.embedding_service import embedding_service
from data.career_paths import CAREER_PATHS_DATA
from data.courses import REAL_COURSES

def run_seed():
    # Drop and recreate tables to ensure fresh start with the new schema
    # (the Course model now includes real-course metadata fields).
    models.Base.metadata.drop_all(bind=database.engine)
    models.Base.metadata.create_all(bind=database.engine)
    
    db = database.SessionLocal()

    print(f"Generating embeddings for {len(REAL_COURSES)} real courses... This might take a minute.")
    seeded = 0
    skipped = 0
    seen_ids = set()
    for course_data in REAL_COURSES:
        course_id = course_data["id"]
        if course_id in seen_ids:
            skipped += 1
            continue
        seen_ids.add(course_id)

        text_to_embed = f"{course_data['title']} - {course_data['description']}"
        course_data["embedding_vector"] = embedding_service.get_embedding(text_to_embed)
        course = models.Course(**course_data)
        db.add(course)
        seeded += 1

    db.commit()
    print(f"Successfully seeded {seeded} real courses with Gemini embeddings"
          + (f" (skipped {skipped} duplicate id(s))." if skipped else "."))

    # Seed career paths
    print("Seeding career paths...")
    for career_data in CAREER_PATHS_DATA:
        career = models.CareerPath(**career_data)
        db.add(career)
    
    db.commit()
    print(f"Successfully seeded {len(CAREER_PATHS_DATA)} career paths.")
    
    db.close()
    print(f"Database seeding complete: {seeded} courses + {len(CAREER_PATHS_DATA)} career paths")

if __name__ == "__main__":
    run_seed()
