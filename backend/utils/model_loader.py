import logging

logger = logging.getLogger(__name__)

class ModelLoader:
    _spacy_model = None

    @classmethod
    def get_spacy_model(cls, model_name="en_core_web_sm"):
        """Lazy loads and returns a shared spaCy model."""
        if cls._spacy_model is None:
            import spacy
            logger.info(f"Loading shared spaCy model: {model_name}...")
            cls._spacy_model = spacy.load(model_name)
            logger.info("Shared spaCy model loaded successfully.")
        return cls._spacy_model
