import requests
from newspaper import Article
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse
import time

class NewsFetcher:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_from_url(self, url, timeout=10):
        """Fetch news content from a URL"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            
            return {
                'title': article.title,
                'text': article.text,
                'summary': article.summary,
                'authors': article.authors,
                'publish_date': article.publish_date,
                'top_image': article.top_image,
                'keywords': article.keywords,
                'url': url,
                'source': urlparse(url).netloc
            }
        except Exception as e:
            print(f"Error fetching from URL {url}: {e}")
            return None
    
    def fetch_from_news_api(self, query, language='en', sort_by='publishedAt', page_size=10):
        """Fetch news using News API"""
        if not self.api_key:
            raise ValueError("News API key is required")
        
        url = f"https://newsapi.org/v2/everything?q={query}&language={language}&sortBy={sort_by}&pageSize={page_size}&apiKey={self.api_key}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for article_data in data.get('articles', []):
                article = self.fetch_from_url(article_data['url'])
                if article:
                    articles.append(article)
            
            return articles
        except Exception as e:
            print(f"Error fetching from News API: {e}")
            return []
    
    def fetch_multiple_sources(self, queries, max_articles=5):
        """Fetch news from multiple sources/queries"""
        all_articles = []
        
        for query in queries:
            articles = self.fetch_from_news_api(query, page_size=max_articles)
            all_articles.extend(articles)
            time.sleep(1)  # Be respectful to the API
        
        return all_articles