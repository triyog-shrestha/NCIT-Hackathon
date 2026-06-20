import torch
import numpy as np
from transformers import AutoTokenizer 
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax 

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"

class SentimentAnalysis:
    def __init__(self):
        """
        Initialize the sentiment analysis model and tokenizer.

        Responsibilities:
        - Load the pretrained tokenizer and sentiment classification model.
        - Detect whether a CUDA-enabled GPU is available.
        - Move the model to the appropriate device (GPU or CPU).
        - Initialize instance variables used throughout the sentiment pipeline.

        Attributes Created:
        - MODEL (str): Hugging Face model identifier.
        - tokenizer: Tokenizer used to preprocess text.
        - model: Pretrained sentiment classification model.
        - device (str): Execution device ('cuda' or 'cpu').
        - text (str | None): Stores the most recently analyzed text.
        """
        self.MODEL = MODEL
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL)
        self.text = None 
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def user_text(self, text: str):
        """
        Analyze user-provided text for sentiment.

        Parameters:
        - text (str):
            The input text to be evaluated.

        Side Effects:
        - Stores the text in self.text.
        - Executes the sentiment analysis pipeline by calling
            polarity_scores().

        Returns:
        - None
        """
        self.text = text
        self.polarity_scores(text)

    def polarity_scores(self, text: str):
        """
        Compute sentiment probabilities for the supplied text.

        Process:
        1. Tokenize the input text.
        2. Move tokenized tensors to the configured device.
        3. Perform model inference without gradient tracking.
        4. Convert model logits into probabilities using softmax.
        5. Classify the dominant sentiment.
        6. Return all sentiment probabilities.

        Parameters:
        - text (str):
            Text to analyze.

        Returns:
        - dict:
            Dictionary containing sentiment probabilities:

            {
                'negative': float,
                'neutral': float,
                'positive': float
            }

        Notes:
        - Probability values range from 0 to 1.
        - The probabilities sum to approximately 1.
        """
        encode_text = self.tokenizer(text, return_tensors='pt')
        encode_text = {k: v.to(self.device) for k, v in encode_text.items()}

        with torch.no_grad():
            output = self.model(**encode_text)

        scores = output.logits[0].cpu().numpy()
        scores = softmax(scores)

        scores_dict = {
            'negative': scores[0],
            'neutral': scores[1],
            'positive': scores[2]
        }
        self.classify(scores_dict)
        return scores_dict
    
    def classify(self, scores: dict):
        """
        Determine the sentiment label with the highest probability.

        Parameters:
        - scores (dict):
            Dictionary containing sentiment probabilities produced
            by polarity_scores().

        Example:
            {
                'negative': 0.12,
                'neutral': 0.18,
                'positive': 0.70
            }

        Behavior:
        - Selects the sentiment with the largest probability.
        - Prints the predicted sentiment label to the console.

        Returns:
        - None
        """
        probabilities = scores 
        predicted_emotion = max(probabilities, key=probabilities.get)
        print(predicted_emotion)