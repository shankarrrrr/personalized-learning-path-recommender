import os
from sqlalchemy.orm import Session
import database, models
from services.embedding_service import embedding_service

def run_seed():
    # Drop and recreate tables to ensure fresh start with embeddings
    models.Base.metadata.drop_all(bind=database.engine)
    models.Base.metadata.create_all(bind=database.engine)
    
    db = database.SessionLocal()
    
    courses_data = [
        {
            "id": "sql_basics",
            "title": "SQL for Data Science",
            "description": "Learn the basics of SQL, including SELECT, WHERE, and JOINs.",
            "domain": "Data",
            "skills_taught": ["sql_basics"],
            "prerequisites": [],
            "level": "Beginner",
            "format": "Video",
            "duration": "4 weeks"
        },
        {
            "id": "python_basics",
            "title": "Python for Everybody",
            "description": "Fundamental programming concepts in Python.",
            "domain": "Data",
            "skills_taught": ["python_basics"],
            "prerequisites": [],
            "level": "Beginner",
            "format": "Interactive",
            "duration": "6 weeks"
        },
        {
            "id": "pandas",
            "title": "Data Manipulation with Pandas",
            "description": "Learn to clean and manipulate data using Python's Pandas library.",
            "domain": "Data",
            "skills_taught": ["pandas"],
            "prerequisites": ["sql_basics", "python_basics"],
            "level": "Intermediate",
            "format": "Project",
            "duration": "4 weeks"
        },
        {
            "id": "machine_learning",
            "title": "Machine Learning Fundamentals",
            "description": "Introduction to supervised and unsupervised learning algorithms.",
            "domain": "Data",
            "skills_taught": ["machine_learning"],
            "prerequisites": ["pandas"],
            "level": "Advanced",
            "format": "Video",
            "duration": "8 weeks"
        }
    ]

    for i in range(1, 47):
        courses_data.append({
            "id": f"mock_course_{i}",
            "title": f"Advanced Topic {i} in Data",
            "description": f"Detailed exploration of advanced data topic {i}.",
            "domain": "Data",
            "skills_taught": [f"advanced_skill_{i}"],
            "prerequisites": ["machine_learning"],
            "level": "Advanced",
            "format": "Reading",
            "duration": "2 weeks"
        })

    print("Generating embeddings for 50 courses... This might take a few seconds.")
    for course_data in courses_data:
        text_to_embed = f"{course_data['title']} - {course_data['description']}"
        course_data["embedding_vector"] = embedding_service.get_embedding(text_to_embed)
        course = models.Course(**course_data)
        db.add(course)

    db.commit()
    print(f"Successfully seeded {len(courses_data)} courses with Gemini embeddings.")
    db.close()

if __name__ == "__main__":
    run_seed()
