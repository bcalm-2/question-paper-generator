from __future__ import annotations

import logging
from utils.cache import ConfigCache

logger = logging.getLogger(__name__)


class SubjectService:
    """
    Handles the lifecycle of subjects and their associated topics.

    Responsibilities (SRP):
        - Subject/topic CRUD only. Does NOT handle HTTP request/response
          objects or any other domain concerns.

    Design patterns:
        - Dependency Injection: receives ``subject_repo`` and ``topic_repo``
          via constructor, making the service independently testable.
    """

    def __init__(self, subject_repo, topic_repo):
        """
        Args:
            subject_repo: Instance of :class:`~repositories.subject_repository.SubjectRepository`.
            topic_repo:   Instance of :class:`~repositories.subject_repository.TopicRepository`.
        """
        self.subject_repo = subject_repo
        self.topic_repo = topic_repo

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_all_subjects(self) -> list[dict]:
        """
        Fetches all subjects with their topics in a single JOIN query.

        Returns:
            Flat list of row dicts — same format as
            :meth:`~repositories.subject_repository.SubjectRepository.get_all_with_topics`.
        """
        return self.subject_repo.get_all_with_topics()

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------

    def add_subject(self, name: str, topics: list[str]) -> tuple[dict, int]:
        """
        Creates a new subject and its topics, then invalidates the cache.

        Args:
            name:   Display name of the subject (required).
            topics: List of topic name strings (may be empty).

        Returns:
            ``(response_dict, http_status_code)``
        """
        if not name:
            return {"error": "Subject name is required"}, 400

        subject_id = self.subject_repo.create(name)
        for topic_name in topics:
            if topic_name:
                self.topic_repo.create(subject_id, topic_name)

        ConfigCache.clear()
        logger.info(f"Subject '{name}' (id={subject_id}) created with {len(topics)} topics.")
        return {"message": "Subject added successfully", "id": subject_id}, 201

    def delete_subject(self, subject_id: int) -> tuple[dict, int]:
        """
        Deletes a subject by ID and invalidates the cache.

        Args:
            subject_id: Primary key of the subject to remove.

        Returns:
            ``(response_dict, http_status_code)``
        """
        self.subject_repo.delete(subject_id)
        ConfigCache.clear()
        logger.info(f"Subject id={subject_id} deleted.")
        return {"message": "Subject deleted successfully"}, 200
