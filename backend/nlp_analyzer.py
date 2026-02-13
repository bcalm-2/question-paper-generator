import spacy
from collections import Counter


class NLPAnalyzer:
    def __init__(self, model="en_core_web_sm"):
        self.nlp = spacy.load(model)

    def analyze(self, text: str):
        doc = self.nlp(text)

        sentences = []
        entities = []
        question_worthy = []

        # Extract entities for better context
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_
            })

        # Process sentences
        for sent in doc.sents:
            sent_text = sent.text.strip()
            if len(sent_text) < 20: continue # Skip too short sentences

            is_worthy, category = self._is_question_worthy(sent)

            if is_worthy:
                formatted_q = self._format_as_question(sent, category)
                sentences.append({
                    "text": sent_text,
                    "question": formatted_q,
                    "category": category
                })
                question_worthy.append({
                    "original": sent_text,
                    "question": formatted_q,
                    "category": category
                })

        # Enhanced keyword extraction (nouns and proper nouns are better for distractors)
        keywords = [
            token.lemma_.lower()
            for token in doc
            if token.is_alpha and not token.is_stop and token.pos_ in ["NOUN", "PROPN"]
        ]
        freq = Counter(keywords)
        top_keywords = [w for w, _ in freq.most_common(20)]

        return {
            "entities": entities,
            "keywords": top_keywords,
            "question_worthy_sentences": question_worthy
        }

    def _is_question_worthy(self, sent):
        """
        Determines if a sentence is suitable for generating a question.
        Returns (bool, category)
        """
        text = sent.text.lower()
        
        # 1. Definition patterns
        if any(w in text for w in [" is a ", " is the ", " refers to ", " is defined as "]):
            return True, "definition"
        
        # 2. Process/Function patterns
        if any(w in text for w in [" used for ", " responsible for ", " provides ", " allows "]):
            return True, "function"
            
        # 3. Comparison
        if any(w in text for w in [" differ from ", " compared to ", " unlike ", " similar to "]):
            return True, "comparison"

        # 4. Importance/Core concepts
        important_verbs = {"manage", "control", "perform", "ensure", "handle", "execute"}
        if any(tok.lemma_.lower() in important_verbs for tok in sent):
            return True, "process"

        return False, None

    def _format_as_question(self, sent, category):
        """
        Attempts to transform a sentence into a question format.
        """
        text = sent.text.strip()
        if text.endswith("."):
            text = text[:-1]

        if category == "definition":
            # Try to extract the subject
            for chunk in sent.noun_chunks:
                return f"Explain the concept of {chunk.text}."
            return f"What is meant by: {text}?"
            
        elif category == "function":
            for chunk in sent.noun_chunks:
                return f"Describe the function of {chunk.text}."
            return f"Describe the function of the following: {text}."
            
        elif category == "comparison":
            return f"Compare and contrast the elements mentioned here: {text}."
            
        elif category == "process":
            return f"Explain the process described: {text}."

        return f"Discuss: {text}."
