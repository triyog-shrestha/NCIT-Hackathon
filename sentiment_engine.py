"""Simple sentiment analysis with emotion history tracking."""

from transformers import pipeline

MODEL = "siebert/sentiment-roberta-large-english"


class SentimentAnalysis:
    """Classifies text sentiment and tracks label history over time."""

    def __init__(self, model: str = MODEL):
        self.pipeline = pipeline("sentiment-analysis", model=model)
        self.history: list[str] = []

    def classify(self, text: str | list[str]) -> list[dict]:
        """Classify a string or list of strings, recording labels to history."""
        results = self.pipeline(text)
        if isinstance(results, dict):
            results = [results]
            self.emotion_history(results)
        return results

    def emotion_history(self)