from __future__ import annotations

"""
Bloom's Taxonomy reference data.

Contains the three artefacts needed to classify and order
cognitive complexity levels in generated questions:

* ``BLOOMS``       — ordered list of the six levels (low → high)
* ``BLOOM_VERBS``  — mapping of each level to its characteristic action verbs
* ``BLOOM_PRIORITY`` — priority order used to select the *highest* matched level
                       (highest cognitive level wins in case of multiple matches)
"""

# Six levels of Bloom's Revised Taxonomy (lowest → highest)
BLOOMS: list[str] = [
    "Remember",
    "Understand",
    "Apply",
    "Analyze",
    "Evaluate",
    "Create",
]

# Action verbs that signal each Bloom level in an educational sentence
BLOOM_VERBS: dict[str, list[str]] = {
    "Remember":  ["define", "list", "recall", "identify", "state"],
    "Understand": ["explain", "describe", "summarize", "interpret"],
    "Apply":     ["solve", "use", "implement", "execute", "calculate"],
    "Analyze":   ["compare", "differentiate", "analyze", "examine"],
    "Evaluate":  ["justify", "critique", "evaluate", "assess"],
    "Create":    ["design", "formulate", "create", "develop", "construct"],
}

# Priority order (highest cognitive level first) used by BloomClassifier
# to pick the single most significant level when multiple verbs match.
BLOOM_PRIORITY: list[str] = [
    "Create",
    "Evaluate",
    "Analyze",
    "Apply",
    "Understand",
    "Remember",
]
