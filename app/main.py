from flask import Flask, render_template, request, jsonify
from app.models.summarizer import TextSummarizer
from app.models.sentiment import SentimentAnalyzer
from app.models.analyzer import NewsAnalyzer
from app.utils.fetcher import NewsFetcher
from app.utils.visualizer import DataVisualizer
from config import Config
import json

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize components
    summarizer = TextSummarizer()
    sentiment_analyzer = SentimentAnalyzer()
    news_analyzer = NewsAnalyzer()
    news_fetcher = NewsFetcher(api_key=app.config['NEWS_API_KEY'])
    visualizer = DataVisualizer()
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/analyze', methods=['POST'])
    def analyze_news():
        try:
            data = request.get_json()
            query = data.get('query', '')
            custom_url = data.get('url', '')
            
            news_articles = []
            
            if custom_url:
                # Analyze single article from URL
                article = news_fetcher.fetch_from_url(custom_url)
                if article:
                    news_articles.append(article)
            else:
                # Fetch news based on query
                news_articles = news_fetcher.fetch_from_news_api(query, page_size=10)
            
            if not news_articles:
                return jsonify({'error': 'No news articles found'}), 404
            
            # Process each article
            results = []
            for article in news_articles:
                # Summarize
                summary = summarizer.summarize(article['text'])
                
                # Analyze sentiment
                sentiment = sentiment_analyzer.analyze_sentiment_transformers(article['text'])
                
                results.append({
                    'title': article['title'],
                    'url': article['url'],
                    'source': article['source'],
                    'summary': summary,
                    'sentiment': sentiment,
                    'publish_date': article['publish_date'].isoformat() if article['publish_date'] else None,
                    'image': article['top_image']
                })
            
            # Overall analysis
            overall_analysis = news_analyzer.analyze_news(news_articles)
            sentiment_stats = sentiment_analyzer.get_sentiment_stats(
                [result['sentiment'] for result in results]
            )
            
            # Generate visualizations
            sentiment_chart = visualizer.create_sentiment_chart(sentiment_stats)
            entity_chart = visualizer.create_entity_chart(overall_analysis['entity_frequencies'])
            wordcloud = visualizer.create_wordcloud(overall_analysis['processed_text'])
            
            # Source comparison
            source_analysis = news_analyzer.compare_sources(news_articles)
            source_chart = visualizer.create_source_comparison_chart(source_analysis)
            
            return jsonify({
                'articles': results,
                'analysis': overall_analysis,
                'visualizations': {
                    'sentiment_chart': sentiment_chart.to_json(),
                    'entity_chart': entity_chart.to_json(),
                    'wordcloud': wordcloud,
                    'source_chart': source_chart.to_json()
                },
                'sentiment_stats': sentiment_stats
            })
            
        except Exception as e:
            app.logger.error(f"Error in analysis: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/summarize', methods=['POST'])
    def summarize_text():
        try:
            data = request.get_json()
            text = data.get('text', '')
            
            if not text:
                return jsonify({'error': 'No text provided'}), 400
            
            summary = summarizer.summarize(text)
            
            return jsonify({
                'original_text': text,
                'summary': summary
            })
            
        except Exception as e:
            app.logger.error(f"Error in summarization: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    return app