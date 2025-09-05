from collections import Counter
import numpy as np
from app.utils.preprocessor import TextPreprocessor

class NewsAnalyzer:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
    
    def analyze_news(self, news_data):
        """Comprehensive analysis of news data"""
        if not news_data:
            return {}
        
        # Extract all text for analysis
        all_text = ' '.join([news.get('text', '') for news in news_data if news.get('text')])
        
        # Preprocess text
        processed_text = self.preprocessor.preprocess(all_text)
        
        # Extract entities
        entities = self.preprocessor.extract_entities(all_text)
        
        # Extract key phrases
        key_phrases = self.preprocessor.extract_key_phrases(all_text, num_phrases=10)
        
        # Calculate entity frequencies
        entity_freq = Counter([entity[0] for entity in entities])
        
        # Calculate topic distribution (simplified)
        topics = self._extract_topics(key_phrases)
        
        return {
            'processed_text': processed_text,
            'entities': entities,
            'key_phrases': key_phrases,
            'entity_frequencies': dict(entity_freq.most_common(20)),
            'topics': topics,
            'total_articles': len(news_data),
            'total_words': len(all_text.split())
        }
    
    def _extract_topics(self, key_phrases):
        """Extract main topics from key phrases"""
        # This is a simplified approach - in production you might use LDA or BERTopic
        topics = {}
        
        # Group related phrases (very basic implementation)
        for phrase in key_phrases:
            if len(phrase) > 3:  # Only consider longer phrases as potential topics
                topics[phrase] = topics.get(phrase, 0) + 1
        
        return dict(sorted(topics.items(), key=lambda x: x[1], reverse=True))
    
    def compare_sources(self, news_data):
        """Compare news across different sources"""
        sources = {}
        
        for news in news_data:
            source = news.get('source', 'unknown')
            if source not in sources:
                sources[source] = []
            sources[source].append(news)
        
        source_analysis = {}
        for source, articles in sources.items():
            source_text = ' '.join([article.get('text', '') for article in articles])
            sentiment = self.preprocessor.analyze_sentiment(source_text)
            
            source_analysis[source] = {
                'article_count': len(articles),
                'avg_sentiment': sentiment,
                'key_topics': self.preprocessor.extract_key_phrases(source_text, num_phrases=5)
            }
        
        return source_analysis