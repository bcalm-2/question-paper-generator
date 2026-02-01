import spacy
from collections import Counter


class NLPAnalyzer:
    def __init__(self, model="en_core_web_sm"):
        self.nlp = spacy.load(model)

    def analyze(self, text: str):
        doc = self.nlp(text)

        sentences = []
        pos_tags = []
        token_tags = []
        entities = []
        noun_chunks = []
        keywords = []
        question_worthy = []

        for token in doc:
            pos_tags.append({
                "text": token.text,
                "pos": token.pos_
            })

            token_tags.append({
                "text": token.text,
                "tag": token.tag_
            })

        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_
            })

        for chunk in doc.noun_chunks:
            noun_chunks.append(chunk.text)

        for sent in doc.sents:
            sent_text = sent.text.strip()

            is_question_worthy = self._is_question_worthy(sent)

            sentences.append({
                "text": sent_text,
                "question_worthy": is_question_worthy
            })

            if is_question_worthy:
                question_worthy.append(sent_text)

        words = [
            token.lemma_.lower()
            for token in doc
            if token.is_alpha and not token.is_stop
        ]

        freq = Counter(words)
        keywords = [w for w, _ in freq.most_common(10)]

        return {
            "sentences": sentences,
            "pos_tags": pos_tags,
            "token_tags": token_tags,
            "entities": entities,
            "keywords": keywords,
            "noun_chunks": noun_chunks,
            "question_worthy_sentences": question_worthy
        }

    def _is_question_worthy(self, sent):
        important_verbs = {"is", "are", "was", "were", "define", "explain", "describe", "compare"}

        has_entity = any(ent for ent in sent.ents)
        has_verb = any(tok.lemma_.lower() in important_verbs for tok in sent)
        long_sentence = len(sent) > 6

        return has_entity or has_verb or long_sentence
