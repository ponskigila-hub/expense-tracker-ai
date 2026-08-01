from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from app.ml.training_data import CATEGORY_EXAMPLES

# Below this confidence, the raw ML prediction is considered unreliable
# (usually means the text has no vocabulary overlap with training data)
# and the keyword fallback takes over instead.
CONFIDENCE_FALLBACK_THRESHOLD = 0.35

DEFAULT_CATEGORY = "Others"

# Small keyword safety net for merchants/words the training set never
# saw. This is deliberately simple (substring match) — it exists to
# catch obvious cases, not to replace the model.
KEYWORD_RULES: dict[str, list[str]] = {
    "Food": ["makan", "resto", "cafe", "kopi", "coffee", "food", "eat", "restaurant", "warung", "kuliner"],
    "Groceries": ["mart", "grocery", "sayur", "pasar", "supermarket"],
    "Transportation": ["gojek", "grab", "taxi", "ojek", "bensin", "parkir", "tol", "fuel", "transport", "uber", "krl", "mrt"],
    "Entertainment": ["game", "cinema", "bioskop", "concert", "konser", "netflix film", "hiburan"],
    "Subscription": ["subscription", "langganan", "premium", "bulanan netflix", "spotify"],
    "Shopping": ["shopee", "tokopedia", "belanja", "shop", "store", "mall"],
    "Bills": ["listrik", "pln", "tagihan", "bill", "internet", "wifi", "pdam", "cicilan", "sewa"],
    "Health": ["dokter", "obat", "apotek", "hospital", "clinic", "gym", "vitamin", "health"],
    "Education": ["kursus", "sekolah", "kuliah", "course", "spp", "buku pelajaran"],
    "Travel": ["hotel", "tiket pesawat", "flight", "airbnb", "liburan", "travel", "visa"],
    "Income": ["gaji", "salary", "bonus", "transfer masuk", "dividen", "cashback", "refund"],
}


def _keyword_fallback(text: str) -> str:

    lowered = text.lower()

    for category, keywords in KEYWORD_RULES.items():
        for kw in keywords:
            if kw in lowered:
                return category

    return DEFAULT_CATEGORY


class CategoryClassifier:
    """
    TF-IDF + Multinomial Naive Bayes classifier trained on a bundled
    example set (see training_data.py). Trained once at process start
    since the dataset is small (~100 rows) and training takes
    milliseconds — no need to persist a pickle for a dataset this size.

    Confidence calibration note: with ~12 balanced categories, the
    "random guess" baseline is already ~1/12 (~0.083), so raw
    predict_proba values in the 0.2-0.3 range are actually meaningful,
    not weak. What matters more than an absolute confidence cutoff is
    whether the input has any real vocabulary overlap with training
    data at all — if it doesn't, Naive Bayes just falls back to class
    priors and its "confidence" is not evidence-based.
    """

    def __init__(self):

        texts = [text for text, _ in CATEGORY_EXAMPLES]
        labels = [label for _, label in CATEGORY_EXAMPLES]

        self._pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 2),
                lowercase=True,
                min_df=1
            )),
            ("clf", MultinomialNB(fit_prior=False, alpha=0.3))
        ])

        self._pipeline.fit(texts, labels)

        vectorizer: TfidfVectorizer = self._pipeline.named_steps["tfidf"]
        self._analyzer = vectorizer.build_analyzer()
        self._vocabulary = set(vectorizer.vocabulary_.keys())

    def _has_vocabulary_overlap(self, text: str) -> bool:

        tokens = self._analyzer(text)

        return any(token in self._vocabulary for token in tokens)

    def predict(self, text: str) -> dict:

        text = text.strip()

        if not text:
            return {
                "category": DEFAULT_CATEGORY,
                "confidence": 0.0,
                "method": "default"
            }

        has_overlap = self._has_vocabulary_overlap(text)

        if has_overlap:

            probabilities = self._pipeline.predict_proba([text])[0]
            classes = self._pipeline.classes_

            best_idx = probabilities.argmax()
            best_category = classes[best_idx]
            best_confidence = float(probabilities[best_idx])

            if best_confidence >= CONFIDENCE_FALLBACK_THRESHOLD:
                return {
                    "category": best_category,
                    "confidence": round(best_confidence, 4),
                    "method": "ml"
                }

            return {
                "category": best_category,
                "confidence": round(best_confidence, 4),
                "method": "ml_low_confidence"
            }

        # No real vocabulary overlap at all — the model has nothing to
        # go on, so don't trust its prior-driven guess. Try keywords,
        # then give up honestly.
        fallback_category = _keyword_fallback(text)

        return {
            "category": fallback_category,
            "confidence": 0.0,
            "method": "keyword_fallback" if fallback_category != DEFAULT_CATEGORY else "default"
        }


# Module-level singleton — trained once when the app imports this module.
category_classifier = CategoryClassifier()
