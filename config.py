#Note: Original values for most of the configurations have been removed.
#Provive your values - To make the app works

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Model settings
    SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
    SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    
    # News API settings
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your_news_api_key_here")
    
    # Application settings
    DEBUG = os.getenv("DEBUG", False)
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    
    # File paths
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
    MODELS_PATH = os.path.join(os.path.dirname(__file__), 'models')
    
    # NLP settings
    MAX_SUMMARY_LENGTH = 150
    MIN_SUMMARY_LENGTH = 30
    NUM_BEAMS = 4