import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class DataVisualizer:
    @staticmethod
    def create_sentiment_chart(sentiment_stats):
        """Create sentiment distribution chart"""
        labels = ['Positive', 'Negative', 'Neutral']
        values = [
            sentiment_stats['positive_count'],
            sentiment_stats['negative_count'],
            sentiment_stats['neutral_count']
        ]
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_layout(title_text='Sentiment Distribution')
        
        return fig
    
    @staticmethod
    def create_entity_chart(entity_freq):
        """Create entity frequency chart"""
        entities = list(entity_freq.keys())[:10]
        frequencies = list(entity_freq.values())[:10]
        
        fig = go.Figure([go.Bar(x=entities, y=frequencies)])
        fig.update_layout(
            title_text='Top Entities',
            xaxis_title="Entities",
            yaxis_title="Frequency"
        )
        
        return fig
    
    @staticmethod
    def create_wordcloud(text):
        """Generate word cloud image"""
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            max_words=100
        ).generate(text)
        
        # Convert to base64 for web display
        img_buffer = BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
        plt.close()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def create_source_comparison_chart(source_analysis):
        """Create chart comparing different news sources"""
        sources = list(source_analysis.keys())
        article_counts = [source_analysis[source]['article_count'] for source in sources]
        sentiment_scores = [source_analysis[source]['avg_sentiment']['score'] for source in sources]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=sources,
            y=article_counts,
            name='Article Count',
            marker_color='lightskyblue'
        ))
        
        fig.add_trace(go.Scatter(
            x=sources,
            y=sentiment_scores,
            name='Sentiment Score',
            yaxis='y2',
            marker=dict(color='red', size=10),
            mode='markers+lines'
        ))
        
        fig.update_layout(
            title_text='News Source Comparison',
            xaxis_title="News Sources",
            yaxis=dict(
                title="Article Count",
                titlefont=dict(color="lightskyblue"),
                tickfont=dict(color="lightskyblue")
            ),
            yaxis2=dict(
                title="Sentiment Score",
                titlefont=dict(color="red"),
                tickfont=dict(color="red"),
                anchor="x",
                overlaying="y",
                side="right"
            )
        )
        
        return fig