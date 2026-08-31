import os
import time
from types import SimpleNamespace

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

# Free-tier Gemini embedding quota is ~100 requests/min. Seed with pacing
# to avoid 429 RESOURCE_EXHAUSTED errors when embedding large catalogues.
EMBED_RPM_LIMIT = int(os.getenv("GEMINI_EMBED_RPM_LIMIT", "60"))
EMBED_MAX_RETRIES = int(os.getenv("GEMINI_EMBED_MAX_RETRIES", "5"))


class EmbeddingService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Expose config as instance attributes for easy introspection/override.
        self.embedding_model = EMBEDDING_MODEL
        self.embedding_dim = EMBEDDING_DIM
        self.rpm_limit = EMBED_RPM_LIMIT
        self.max_retries = EMBED_MAX_RETRIES
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

        # In-memory vector store mapping: course_id -> numpy vector
        self.course_index = {}
        self.is_initialized = False
        # Simple in-memory cache to avoid re-embedding identical query strings.
        self._query_cache = {}
        # Track request timestamps to self-throttle to the configured RPM.
        self._request_times: list[float] = []
        # Cached list of Course ORM objects (avoids repeated DB round-trips).
        self._cached_courses = None
    def _throttle(self) -> None:
        """Sleep if necessary to stay within the configured requests-per-minute limit."""
        if self.rpm_limit <= 0:
            return
        now = time.monotonic()
        # Drop timestamps older than 60s.
        self._request_times = [t for t in self._request_times if now - t < 60.0]
        if len(self._request_times) >= self.rpm_limit:
            sleep_for = 60.0 - (now - self._request_times[0]) + 0.1
            if sleep_for > 0:
                print(f"[embedding] RPM limit reached, sleeping {sleep_for:.1f}s...")
                time.sleep(sleep_for)
            now = time.monotonic()
            self._request_times = [t for t in self._request_times if now - t < 60.0]
        self._request_times.append(time.monotonic())

    def get_embedding(self, text: str) -> list:
        """Generate an embedding for the given text using Gemini, with retry + pacing."""
        if not self.client:
            # Fallback mock embedding (zero vector of the configured dimension)
            return [0.0] * self.embedding_dim

        # Return cached embedding if we already embedded this exact text.
        if text in self._query_cache:
            return self._query_cache[text]

        last_err: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            self._throttle()
            try:
                response = self.client.models.embed_content(
                    model=self.embedding_model,
                    contents=text,
                    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
                )
                embedding = response.embeddings[0].values
                self._query_cache[text] = embedding
                return embedding
            except Exception as e:  # noqa: BLE001 - broad catch for rate-limit/network
                last_err = e
                msg = str(e)
                # 429 RESOURCE_EXHAUSTED or transient server errors -> back off.
                if "429" in msg or "RESOURCE_EXHAUSTED" in msg or "503" in msg:
                    backoff = min(2 ** attempt, 60)
                    print(f"[embedding] rate limited/transient error (attempt {attempt}), "
                          f"retrying in {backoff}s: {msg[:120]}")
                    time.sleep(backoff)
                    continue
                # Non-retryable error; re-raise immediately.
                raise
        # Exhausted retries.
        raise RuntimeError(f"Embedding generation failed after {self.max_retries} attempts: {last_err}")

    def build_course_index(self, db_session):
        """Load all courses from the DB and cache their vectors + snapshots.

        IMPORTANT: we cache plain dict snapshots, NOT the ORM objects. ORM
        objects are bound to the session that loaded them; once that request's
        session closes, any later access to an expired attribute (e.g.
        course.skills_taught) triggers a DetachedInstanceError. By snapshotting
        the fields we need into dicts here, the cache becomes fully session-
        independent and safe to reuse across requests.
        """
        # Local import to avoid circular dependency
        import models
        courses = db_session.query(models.Course).all()
        snapshots = []
        count = 0
        for course in courses:
            # Eagerly read every field downstream code touches while the
            # session is still alive, then store a detached dict.
            if course.embedding_vector:
                # Convert the JSON list to a fast numpy array
                self.course_index[course.id] = np.array(course.embedding_vector)
                count += 1
            snapshots.append(self._snapshot_course(course))
        self._cached_courses = snapshots
        self.is_initialized = True
        print(f"Loaded {count} course vectors into memory.")

    @staticmethod
    def _snapshot_course(course) -> SimpleNamespace:
        """Return a session-independent snapshot of a Course ORM object.

        Reads all attributes the recommendation/roadmap code depends on while
        the object is still attached to its session, then returns a detached
        SimpleNamespace. SimpleNamespace supports the same `.attr` access as
        the ORM object, so downstream code (recommendation_service.retrieve_
        best_course, main.py) works unchanged while the snapshot stays valid
        across requests even after the originating session has closed.
        """
        return SimpleNamespace(
            id=course.id,
            title=course.title,
            description=course.description,
            domain=course.domain,
            skills_taught=list(course.skills_taught or []),
            prerequisites=list(course.prerequisites or []),
            level=course.level,
            format=course.format,
            duration=course.duration,
            platform=course.platform,
            course_url=course.course_url,
            instructor=course.instructor,
            rating=course.rating,
            rating_count=course.rating_count,
            price=course.price,
            is_free=course.is_free,
            language=course.language,
        )

    def get_cached_courses(self, db_session) -> list:
        """Return the cached course snapshots, rebuilding the index if needed.

        Always returns plain dicts (never ORM objects), so callers can safely
        read attributes without an active session.
        """
        if not self.is_initialized or not self._cached_courses:
            self.build_course_index(db_session)
        return self._cached_courses

embedding_service = EmbeddingService()
