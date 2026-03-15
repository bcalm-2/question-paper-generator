from utils.model_loader import ModelLoader
from constants import BLOOM_VERBS, BLOOM_PRIORITY


class BloomClassifier:

    def __init__(self):
        self.bloom_verbs = BLOOM_VERBS
        self.priority = BLOOM_PRIORITY

    def _get_nlp(self):
        return ModelLoader.get_spacy_model()

    def _get_lemmatizer(self):
        return ModelLoader.get_lemmatizer()

    def _get_wordnet(self):
        return ModelLoader.get_wordnet()

    def extract_verbs(self, sentence):
        doc = self._get_nlp()(sentence)
        verbs = []

        for token in doc:
            if token.pos_ == "VERB" and token.dep_ != "aux":
                verbs.append(token.text)

        return verbs

    def lemmatize_verbs(self, verbs):
        lemmatizer = self._get_lemmatizer()
        wordnet = self._get_wordnet()
        return [
            lemmatizer.lemmatize(v.lower(), wordnet.VERB)
            for v in verbs
        ]

    def get_default_level(self):
        return "Understand"

    def classify(self, sentence):
        verbs = self.extract_verbs(sentence)
        lemmas = self.lemmatize_verbs(verbs)

        matched_levels = set()

        for level, bloom_verbs in self.bloom_verbs.items():
            for v in lemmas:
                if v in bloom_verbs:
                    matched_levels.add(level)

        # Apply priority
        for level in self.priority:
            if level in matched_levels:
                return level

        return self.get_default_level()


