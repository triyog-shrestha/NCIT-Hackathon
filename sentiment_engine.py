from transformers import AutoTokenizer 
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax 

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"

class SentimentAnalysis:
    def __init__(self):
        self.MODEL = MODEL
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL)
        self.text = None 
    def user_text(self, text: str):
        self.text = text
        self._encode_text(text)
    def _encode_text(self, text: str):
        encode_text = self.tokenizer(text, return_tensors='pt') 
        output = self.model(**encode_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        scores_dict = {
            'negative' : scores[0],
            'neutral' : scores[1],
            'positive' : scores[2]
        }
        print(scores_dict)