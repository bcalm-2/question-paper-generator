import logging

logger = logging.getLogger(__name__)

class ConfigCache:
    _cache = {}

    @classmethod
    def get(cls, key):
        return cls._cache.get(key)

    @classmethod
    def set(cls, key, data):
        cls._cache[key] = data

    @classmethod
    def clear(cls):
        logger.info("Clearing configuration cache")
        cls._cache = {}
