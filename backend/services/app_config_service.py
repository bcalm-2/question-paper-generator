import logging
from config.bloom_taxonomy import BLOOMS
from utils.cache import ConfigCache

logger = logging.getLogger(__name__)

class AppConfigService:
    """
    Service responsible for providing and caching application configuration.
    Decouples configuration assembly from route handlers.
    """
    def __init__(self, subject_repo):
        self.subject_repo = subject_repo

    def get_app_config(self):
        """
        Fetches, formats, and caches application configuration including subjects, topics, and Bloom's levels.
        """
        cached_config = ConfigCache.get("user_config")
        if cached_config:
            logger.info("Serving configuration from cache")
            return cached_config

        logger.info("Assembling application configuration from database")
        
        # Optimized single JOIN query from repo
        flat_data = self.subject_repo.get_all_with_topics()
        
        subjects = []
        subject_topics = {}
        seen_subjects = set()
        
        for row in flat_data:
            sub_id = row['subject_id']
            sub_name = row['subject_name']
            topic_name = row['topic_name']
            
            if sub_id not in seen_subjects:
                subjects.append({"id": sub_id, "name": sub_name})
                subject_topics[sub_name] = []
                seen_subjects.add(sub_id)
                
            if topic_name:
                subject_topics[sub_name].append(topic_name)

        config = {
            "SUBJECT_TOPICS": subject_topics, # Frontend compatibility
            "SUBJECTS": subjects,             # Detailed access
            "BLOOMS": BLOOMS
        }
        
        ConfigCache.set("user_config", config)
        return config

    def get_admin_subjects(self):
        """
        Fetches full-detail subject data including topic IDs and descriptions for administrative use.
        Uses optimized database queries and caching.
        """
        cached = ConfigCache.get("admin_subjects")
        if cached:
            return cached

        flat_data = self.subject_repo.get_all_with_topics()
        subjects_dict = {}
        
        for row in flat_data:
            sub_id = row['subject_id']
            if sub_id not in subjects_dict:
                subjects_dict[sub_id] = {
                    "id": sub_id,
                    "name": row['subject_name'],
                    "description": row['subject_description'],
                    "topics": []
                }
            
            if row['topic_name']:
                subjects_dict[sub_id]['topics'].append({
                    "id": row['topic_id'],
                    "name": row['topic_name']
                })
        
        subjects_list = list(subjects_dict.values())
        ConfigCache.set("admin_subjects", subjects_list)
        return subjects_list

