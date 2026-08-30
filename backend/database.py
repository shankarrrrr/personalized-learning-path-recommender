from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL is configurable so Docker can mount a persistent volume.
# Defaults to a local SQLite file for development.
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    os.getenv("SQLITE_DB_PATH", "sqlite:///./sql_app.db"),
    # If SQLITE_DB_PATH is set without sqlite:///, normalize it.
)
if SQLALCHEMY_DATABASE_URL.endswith(".db") and not SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    SQLALCHEMY_DATABASE_URL = "sqlite:///" + SQLALCHEMY_DATABASE_URL

# check_same_thread=False is only valid for SQLite; skip for other DBs.
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
