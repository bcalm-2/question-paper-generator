from utils.model_loader import ModelLoader
from constants import BLOOM_VERBS, BLOOM_PRIORITY


class BloomClassifier:

    def __init__(self):
        self.bloom_verbs = BLOOM_VERBS
        self.priority = BLOOM_PRIORITY

    def _get_nlp(self):
        return ModelLoader.get_spacy_model()

    def extract_lemmas(self, doc_or_sent):
        """Extracts lemmas from a spaCy Doc or Span."""
        return [
            token.lemma_.lower()
            for token in doc_or_sent
            if token.pos_ == "VERB" and token.dep_ != "aux"
        ]

    def get_default_level(self):
        return "Understand"

    def classify_from_doc(self, doc_or_sent):
        """Classifies from a pre-processed spaCy object to save time."""
        lemmas = self.extract_lemmas(doc_or_sent)
        matched_levels = set()

        for level, bloom_verbs in self.bloom_verbs.items():
            for v in lemmas:
                if v in bloom_verbs:
                    matched_levels.add(level)

        for level in self.priority:
            if level in matched_levels:
                return level

        return self.get_default_level()

    def classify(self, sentence):
        """Legacy standalone classification (slower as it runs spaCy)."""
        doc = self._get_nlp()(sentence)
        return self.classify_from_doc(doc)
