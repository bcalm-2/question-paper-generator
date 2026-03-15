import logging

logger = logging.getLogger(__name__)

class ModelLoader:
    _spacy_model = None
    _lemmatizer = None

    @classmethod
    def get_spacy_model(cls, model_name="en_core_web_sm"):
        """Lazy loads and returns a shared spaCy model."""
        if cls._spacy_model is None:
            import spacy
            logger.info(f"Loading shared spaCy model: {model_name}...")
            cls._spacy_model = spacy.load(model_name)
            logger.info("Shared spaCy model loaded successfully.")
        return cls._spacy_model

    @classmethod
    def get_lemmatizer(cls):
        """Lazy loads and returns a shared NLTK WordNet lemmatizer."""
        if cls._lemmatizer is None:
            import nltk
            from nltk.stem import WordNetLemmatizer
            
            logger.info("Loading NLTK WordNet data...")
            # We assume these are already downloaded in the build phase
            # But we call download here as a safety measure (fast if exists)
            try:
                # Suppress output during request handling
                nltk.download('wordnet', quiet=True)
                nltk.download('omw-1.4', quiet=True)
            except Exception as e:
                logger.warning(f"NLTK download check failed: {e}")
                
            cls._lemmatizer = WordNetLemmatizer()
            logger.info("Lemmatizer initialized.")
        return cls._lemmatizer

    @classmethod
    def get_wordnet(cls):
        """Lazy access to wordnet corpus to prevent initial heavy load."""
        from nltk.corpus import wordnet
        return wordnet
