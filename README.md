# NewsNexus - Smart News Analyzer & Summarizer

NewsNexus is an advanced NLP-powered web application that analyzes and summarizes news articles using state-of-the-art machine learning models.

## Features

* **Smart News Analysis**: Fetch and analyze news articles by topic or URL
* **AI-Powered Summarization**: Generate concise summaries using BART transformer model
* **Sentiment Analysis**: Determine positive/negative/neutral sentiment using RoBERTa
* **Entity Recognition**: Extract and visualize key entities and topics
* **Source Comparison**: Compare coverage across different news sources
* **Interactive Visualizations**: Beautiful charts and word clouds

## Technology Stack

* **Backend**: Flask, Python
* **NLP Models**: Hugging Face Transformers (BART, RoBERTa)
* **Frontend**: HTML5, CSS3, JavaScript, Plotly
* **News Processing**: Newspaper3k, BeautifulSoup
* **Data Visualization**: Plotly, WordCloud

## Installation

1. Clone the repository:

```bash
git clone https://github.com/RavenAI/news-nexus.git
cd news-nexus
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Set up environment variables:

```bash
export NEWS_API_KEY=your_news_api_key_here
export DEBUG=True
export SECRET_KEY=your_secret_key_here
```

4. Run the application:

```bash
python run.py
```

5. Open your browser and navigate to [http://localhost:5000](http://localhost:5000)

## Usage

### News Analysis

* Enter a topic or keywords in the search box
* Or provide a specific news article URL
* Click "Analyze News" to process the content
* View analysis results, visualizations, and article summaries

### Text Summarization

* Paste any text into the summarization textarea
* Click "Summarize Text" to generate a concise summary
* View the summary along with length statistics

### API Configuration

To use the news fetching functionality, you need a News API key:

* Sign up at [News API](https://newsapi.org/)
* Get your API key from the dashboard
* Set it as an environment variable or in the `config.py` file

## Project Structure

```
NewsNexus/
├── app/                 # Flask application
│   ├── models/         # NLP models (summarizer, sentiment, analyzer)
│   ├── utils/          # Utility functions (preprocessing, fetching)
│   ├── static/         # CSS and JavaScript files
│   ├── templates/      # HTML templates
│   └── tests/          # Unit tests
├── data/               # Data storage
├── models/             # Saved model files
├── config.py           # Application configuration
├── requirements.txt    # Python dependencies
└── run.py              # Application entry point
```

## Model Information

* **Summarization**: Facebook's BART-large-CNN model
* **Sentiment Analysis**: CardiffNLP's Twitter-RoBERTa-base-sentiment
* **Entity Recognition**: spaCy's en\_core\_web\_sm model

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

* Hugging Face for transformer models
* News API for news data
* spaCy for NLP capabilities
* Plotly for visualization components

---

This implementation provides a complete, modern news analysis and summarization application with:

1. **Modern Architecture**: Well-organized Flask application with proper separation of concerns
2. **Advanced NLP**: Uses state-of-the-art transformer models for summarization and sentiment analysis
3. **Beautiful UI**: Responsive design with interactive visualizations
4. **Comprehensive Features**: News fetching, analysis, summarization, and visualization
5. **Production Ready**: Includes configuration management, error handling, and testing structure

### Quick Start

1. Install the dependencies from `requirements.txt`
2. Set up your News API key
3. Run `python run.py`
4. Open [http://localhost:5000](http://localhost:5000) in your browser

The application will handle model downloads automatically on first run.

Feel free to customize and extend the functionality as needed!

Note: .gitignore file is currently not included in this snippet. Make sure to add one to exclude `venv/`, `__pycache__/`, and other unnecessary files from version control.
