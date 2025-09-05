from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from textblob import TextBlob
import torch
from config import Config

class SentimentAnalyzer:
    def __init__(self):
        self.config = Config()
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Load transformer-based sentiment model
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.config.SENTIMENT_MODEL)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.config.SENTIMENT_MODEL)
            self.analyzer = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device
            )
        except Exception as e:
            print(f"Error loading sentiment model: {e}")
            self.analyzer = None
    
    def analyze_sentiment_transformers(self, text):
        """Analyze sentiment using transformer model"""
        if not self.analyzer:
            return self.analyze_sentiment_textblob(text)
        
        try:
            result = self.analyzer(text[:512])[0]  # Truncate to model max length
            return {
                'label': result['label'],
                'score': result['score'],
                'method': 'transformer'
            }
        except Exception as e:
            print(f"Error in transformer sentiment analysis: {e}")
            return self.analyze_sentiment_textblob(text)
    
    def analyze_sentiment_textblob(self, text):
        """Analyze sentiment using TextBlob (fallback)"""
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.1:
            label = 'POSITIVE'
        elif polarity < -0.1:
            label = 'NEGATIVE'
        else:
            label = 'NEUTRAL'
        
        return {
            'label': label,
            'score': abs(polarity),
            'method': 'textblob'
        }
    
    def analyze_sentiment_batch(self, texts):
        """Analyze sentiment for multiple texts"""
        return [self.analyze_sentiment_transformers(text) for text in texts]
    
    def get_sentiment_stats(self, sentiment_results):
        """Calculate sentiment statistics"""
        labels = [result['label'] for result in sentiment_results]
        
        return {
            'positive_count': labels.count('POSITIVE'),
            'negative_count': labels.count('NEGATIVE'),
            'neutral_count': labels.count('NEUTRAL'),
            'total': len(labels)
        }