from __future__ import annotations

from utils.model_loader import ModelLoader
from collections import Counter


class NLPAnalyzer:
    """
    Core NLP engine for analyzing educational text and identifying question-worthy segments.

    Uses spaCy for POS tagging, NER, and dependency parsing.

    Responsibilities (SRP):
        - Text analysis only. Does NOT handle file I/O or question formatting.
    """

    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initializes the analyzer with a specific spaCy model name."""
        self.model_name = model_name

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze(self, text: str, classifier=None) -> dict:
        """
        Performs full NLP analysis on the provided text.

        Steps:
            1. Extract Named Entities
            2. Segment sentences and evaluate question-worthiness
            3. Identify keywords for distractor generation
            4. Classify Bloom's taxonomy levels (if classifier is provided)

        Args:
            text: Raw text content extracted from a reference file.
            classifier: Optional :class:`BloomClassifier` instance.

        Returns:
            dict with keys ``entities``, ``keywords``, and
            ``question_worthy_sentences``.
        """
        nlp = self._get_model()
        doc = nlp(text)

        entities = []
        question_worthy = []

        # 1. Named Entities
        for ent in doc.ents:
            entities.append({"text": ent.text, "label": ent.label_})

        # 2. Sentence-level analysis
        for sent in doc.sents:
            sent_text = sent.text.strip()
            if len(sent_text) < 20:
                continue  # skip trivially short sentences

            is_worthy, category = self._is_question_worthy(sent)
            if not is_worthy:
                continue

            formatted_q = self._format_as_question(sent, category)
            bloom_level = (
                classifier.classify_from_doc(sent) if classifier else "Understand"
            )

            noun_chunks = list(sent.noun_chunks)
            subject = noun_chunks[0].text if noun_chunks else None

            question_worthy.append(
                {
                    "original": sent_text,
                    "question": formatted_q,
                    "category": category,
                    "subject": subject,
                    "bloom_level": bloom_level,
                }
            )

        # 3. Keyword extraction (nouns + proper nouns are best for distractors)
        keywords = [
            token.lemma_.lower()
            for token in doc
            if token.is_alpha
            and not token.is_stop
            and token.pos_ in {"NOUN", "PROPN"}
        ]
        freq = Counter(keywords)
        top_keywords = [w for w, _ in freq.most_common(20)]

        return {
            "entities": entities,
            "keywords": top_keywords,
            "question_worthy_sentences": question_worthy,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_model(self):
        """Lazy-loads and returns the shared spaCy model."""
        return ModelLoader.get_spacy_model(self.model_name)

    def _is_question_worthy(self, sent) -> tuple[bool, str | None]:
        """
        Determines whether a sentence is suitable for question generation.

        Returns:
            Tuple of ``(is_worthy: bool, category: str | None)``.
        """
        text = sent.text.lower()

        if any(w in text for w in [" is a ", " is the ", " refers to ", " is defined as "]):
            return True, "definition"

        if any(w in text for w in [" used for ", " responsible for ", " provides ", " allows "]):
            return True, "function"

        if any(w in text for w in [" differ from ", " compared to ", " unlike ", " similar to "]):
            return True, "comparison"

        important_verbs = {"manage", "control", "perform", "ensure", "handle", "execute"}
        if any(tok.lemma_.lower() in important_verbs for tok in sent):
            return True, "process"

        return False, None

    def _format_as_question(self, sent, category: str) -> str:
        """
        Heuristically transforms a declarative sentence into an exam question.

        Args:
            sent: A spaCy ``Span`` representing the sentence.
            category: Category returned by :meth:`_is_question_worthy`.

        Returns:
            A formatted question string.
        """
        text = sent.text.strip().rstrip(".")

        if category == "definition":
            for chunk in sent.noun_chunks:
                return f"Explain the concept of {chunk.text}."
            return f"What is meant by: {text}?"

        if category == "function":
            for chunk in sent.noun_chunks:
                return f"Describe the function of {chunk.text}."
            return f"Describe the function of the following: {text}."

        if category == "comparison":
            return f"Compare and contrast the elements mentioned here: {text}."

        if category == "process":
            return f"Explain the process described: {text}."

        return f"Discuss: {text}."
