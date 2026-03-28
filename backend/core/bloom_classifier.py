from __future__ import annotations

from utils.model_loader import ModelLoader
from config.bloom_taxonomy import BLOOM_VERBS, BLOOM_PRIORITY


class BloomClassifier:
    """
    Classifies educational content according to Bloom's Taxonomy.

    Uses verb-based mapping combined with a priority hierarchy to determine
    the cognitive complexity of a given sentence or document.

    Responsibilities (SRP):
        - Bloom level classification only. Does NOT interact with the
          database, filesystem, or Flask request context.
    """

    def __init__(self):
        """Initializes the classifier with Bloom's verb lists and priority order."""
        self.bloom_verbs: dict[str, list[str]] = BLOOM_VERBS
        self.priority: list[str] = BLOOM_PRIORITY

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify_from_doc(self, doc_or_sent) -> str:
        """
        High-performance classification using an already-parsed spaCy Doc or Span.

        Avoids re-parsing by working directly on the provided NLP object.
        Returns the highest-priority Bloom level matched, or the default level.

        Args:
            doc_or_sent: A spaCy ``Doc`` or ``Span``.

        Returns:
            A Bloom's taxonomy level string (e.g. ``"Apply"``).
        """
        lemmas = self._extract_verb_lemmas(doc_or_sent)
        matched_levels = {
            level
            for level, verbs in self.bloom_verbs.items()
            if any(v in verbs for v in lemmas)
        }

        for level in self.priority:
            if level in matched_levels:
                return level

        return self.get_default_level()

    def classify(self, sentence: str) -> str:
        """
        Convenience method for classifying a raw sentence string.

        Note: Slower than :meth:`classify_from_doc` because it triggers a
        full spaCy parse. Prefer ``classify_from_doc`` when a parsed Doc/Span
        is already available (e.g. during batch NLP analysis).

        Args:
            sentence: Plain-text sentence to classify.

        Returns:
            A Bloom's taxonomy level string.
        """
        doc = self._get_nlp()(sentence)
        return self.classify_from_doc(doc)

    def get_default_level(self) -> str:
        """Returns the fallback Bloom level when no verbs match."""
        return "Understand"

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_nlp(self):
        """Lazy-loads the shared spaCy model via :class:`ModelLoader`."""
        return ModelLoader.get_spacy_model()

    def _extract_verb_lemmas(self, doc_or_sent) -> list[str]:
        """
        Extracts non-auxiliary verb lemmas from a spaCy Doc or Span.

        Args:
            doc_or_sent: A spaCy ``Doc`` or ``Span``.

        Returns:
            List of lowercase lemma strings for content verbs.
        """
        return [
            token.lemma_.lower()
            for token in doc_or_sent
            if token.pos_ == "VERB" and token.dep_ != "aux"
        ]
