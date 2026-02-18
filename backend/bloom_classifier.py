import spacy
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

nltk.download('wordnet')
nltk.download('omw-1.4')

from constants import BLOOM_VERBS, BLOOM_PRIORITY


class BloomClassifier:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.lemmatizer = WordNetLemmatizer()
        self.bloom_verbs = BLOOM_VERBS
        self.priority = BLOOM_PRIORITY

    def extract_verbs(self, sentence):
        doc = self.nlp(sentence)
        verbs = []

        for token in doc:
            if token.pos_ == "VERB" and token.dep_ != "aux":
                verbs.append(token.text)

        return verbs

    def lemmatize_verbs(self, verbs):
        return [
            self.lemmatizer.lemmatize(v.lower(), wordnet.VERB)
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


