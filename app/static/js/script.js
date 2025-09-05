class NewsNexus {
    constructor() {
        this.initEventListeners();
    }

    initEventListeners() {
        const analyzeForm = document.getElementById('analyzeForm');
        const summarizeForm = document.getElementById('summarizeForm');

        analyzeForm.addEventListener('submit', (e) => this.handleAnalysis(e));
        summarizeForm.addEventListener('submit', (e) => this.handleSummarization(e));
    }

    async handleAnalysis(e) {
        e.preventDefault();
        
        const query = document.getElementById('query').value;
        const url = document.getElementById('url').value;
        
        this.showLoading('analysis');
        this.hideError();
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query, url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Analysis failed');
            }

            this.displayResults(data);
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading('analysis');
        }
    }

    async handleSummarization(e) {
        e.preventDefault();
        
        const text = document.getElementById('textToSummarize').value;
        
        this.showLoading('summarization');
        this.hideError();
        
        try {
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Summarization failed');
            }

            this.displaySummary(data);
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading('summarization');
        }
    }

    displayResults(data) {
        this.displayArticles(data.articles);
        this.displayVisualizations(data.visualizations);
        this.displayAnalysis(data.analysis, data.sentiment_stats);
    }

    displayArticles(articles) {
        const container = document.getElementById('articlesContainer');
        container.innerHTML = '';

        articles.forEach(article => {
            const articleElement = this.createArticleElement(article);
            container.appendChild(articleElement);
        });
    }

    createArticleElement(article) {
        const div = document.createElement('div');
        div.className = 'article-card';
        
        const sentimentClass = `sentiment-${article.sentiment.label.toLowerCase()}`;
        
        div.innerHTML = `
            <div class="article-header">
                <div>
                    <h3 class="article-title">${article.title}</h3>
                    <p class="article-source">${article.source} • ${new Date(article.publish_date).toLocaleDateString()}</p>
                </div>
                <span class="article-sentiment ${sentimentClass}">
                    ${article.sentiment.label}
                </span>
            </div>
            <p class="article-summary">${article.summary}</p>
            <a href="${article.url}" target="_blank" class="article-link">Read full article</a>
        `;
        
        return div;
    }

    displayVisualizations(visualizations) {
        this.renderChart('sentimentChart', JSON.parse(visualizations.sentiment_chart));
        this.renderChart('entityChart', JSON.parse(visualizations.entity_chart));
        this.renderChart('sourceChart', JSON.parse(visualizations.source_chart));
        
        const wordcloudContainer = document.getElementById('wordcloudContainer');
        wordcloudContainer.innerHTML = `<img src="${visualizations.wordcloud}" alt="Word Cloud">`;
    }

    renderChart(containerId, chartData) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        
        Plotly.newPlot(containerId, chartData.data, chartData.layout, {
            responsive: true,
            displayModeBar: true
        });
    }

    displayAnalysis(analysis, sentimentStats) {
        const analysisDiv = document.getElementById('analysisResults');
        
        analysisDiv.innerHTML = `
            <div class="analysis-section">
                <h3>Analysis Overview</h3>
                <p>Total Articles: ${analysis.total_articles}</p>
                <p>Total Words Processed: ${analysis.total_words.toLocaleString()}</p>
                <p>Positive Sentiment: ${sentimentStats.positive_count}</p>
                <p>Negative Sentiment: ${sentimentStats.negative_count}</p>
                <p>Neutral Sentiment: ${sentimentStats.neutral_count}</p>
            </div>
            <div class="analysis-section">
                <h4>Key Topics</h4>
                <div class="topics-list">
                    ${Object.entries(analysis.topics).slice(0, 5).map(([topic, count]) => `
                        <span class="topic-tag">${topic} (${count})</span>
                    `).join('')}
                </div>
            </div>
        `;
    }

    displaySummary(data) {
        const summaryDiv = document.getElementById('summaryResult');
        summaryDiv.innerHTML = `
            <h3>Summary</h3>
            <p>${data.summary}</p>
            <div class="summary-stats">
                <p>Original length: ${data.original_text.split(' ').length} words</p>
                <p>Summary length: ${data.summary.split(' ').length} words</p>
            </div>
        `;
    }

    showLoading(type) {
        document.getElementById(`${type}Loading`).style.display = 'block';
    }

    hideLoading(type) {
        document.getElementById(`${type}Loading`).style.display = 'none';
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }

    hideError() {
        document.getElementById('errorMessage').style.display = 'none';
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new NewsNexus();
});