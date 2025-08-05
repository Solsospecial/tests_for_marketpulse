import streamlit as st
import feedparser
import requests
import random
import pandas as pd
from datetime import datetime
from dateutil import parser
import re
from collections import Counter
from io import BytesIO
import hashlib

# Visualization libraries
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.graph_objects as go

# NLP libraries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings('ignore')

# Module-level cached functions (better than class method caching)
@st.cache_data(ttl=300)
def _scrape_rss_feed(url, max_articles=50):
    """Scrape articles from RSS feed and sort by recency"""
    try:
        feed = feedparser.parse(url)
        articles = []
        
        for entry in feed.entries:
            # Parse the published date for sorting
            published_date_parsed = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    published_date_parsed = datetime(*entry.published_parsed[:6])
                except:
                    pass
        
            # Fallback: try to parse published string
            published = entry.get('published', '')
            if not published_date_parsed and published:
                try:
                    published_date_parsed = parser.parse(published)
                except:
                    pass
            
            raw_title = entry.get('title', '')
            # Skip articles with invalid/missing titles
            if not raw_title or pd.isna(raw_title):
                continue
            
            # Clean the title by removing trailing ' - Source Name'
            clean_title = str(raw_title.rsplit(' - ', 1)[0]).strip() if ' - ' in raw_title else str(raw_title).strip()
            # Skip if title is empty, 'nan', 'None', or too short
            if (not clean_title or clean_title.lower() in ['nan', 'none', 'null', ''] or len(clean_title) < 5):
                continue
                
            # Get and validate source
            source = entry.get('source', {})
            if isinstance(source, dict):
                source_name = source.get('title', 'Unknown')
            else:
                source_name = str(source).strip() if source else 'Unknown'
            if source_name.lower() in ['nan', 'none', 'null']:
                source_name = 'Unknown'
                
            # Get and validate link
            link = entry.get('link', '')
            link = '' if (not link or pd.isna(link)) else str(link).strip()
            
            # Get and validate summary
            summary = entry.get('summary', '')
            summary = '' if (not summary or pd.isna(summary)) else str(summary).strip()
            
            article = {
                'title': clean_title,
                'link': link,
                'published': published,
                'published_date_parsed': published_date_parsed,  # Helper field for sorting
                'summary': summary,
                'source': source_name
            }
            articles.append(article)
            
        # Sort by published date (most recent first)
        articles.sort(key=lambda x: x['published_date_parsed'] or datetime.min, reverse=True)
    
        # Remove helper field and return limited results
        for article in articles:
            del article['published_date_parsed']
    
        return articles[:max_articles]

    except Exception as e:
        st.error(f"Error scraping feed: {str(e)}")
        return []

@st.cache_data(ttl=300)
def _analyze_sentiment_hf(text, model_name="cardiffnlp/twitter-roberta-base-sentiment-latest"):
    """Analyze sentiment using Hugging Face model"""
    try:
        analyzer = pipeline("sentiment-analysis", model=model_name)
        return analyzer(text)[0]["label"]
    except:
        return None

@st.cache_data(ttl=300)
def _analyze_sentiment_vader(text):
    """Analyze sentiment using VADER"""
    analyzer = SentimentIntensityAnalyzer()
    compound_score = analyzer.polarity_scores(text)['compound']
    if compound_score >= 0.05:
        return "positive"
    elif compound_score > -0.05:
        return "neutral"
    else:
        return "negative"

@st.cache_data(ttl=300)
def _summarize_text(text, model_name="facebook/bart-large-cnn"):
    """Summarize text using Hugging Face model"""
    try:
        summarizer = pipeline("summarization", 
                            model=model_name,
                            max_length=150, 
                            min_length=30,
                            do_sample=False)
        return summarizer(text)[0]['summary_text']
    except:
        try:
            # Fallback to smaller model
            summarizer = pipeline("summarization",
                                model="sshleifer/distilbart-cnn-12-6",
                                max_length=120,
                                min_length=25)
            return summarizer(text)[0]['summary_text']
        except:
            return None

@st.cache_data(ttl=300)
def _create_wordcloud_data(text_list, exclude_words_tuple=(), colormap='viridis'):
    """Generate word cloud data (cached separately from visualization)"""
    # Clean and combine text
    text = ' '.join(text_list).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Remove common words
    exclude_words = set(exclude_words_tuple) | {'news', 'says', 'new', 'get', 'make', 'take'}
    words = [word for word in text.split() if len(word) > 1 and word not in exclude_words]
    text = ' '.join(words)
    
    if not text.strip():
        return None
        
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap=colormap,
        max_words=100,
        relative_scaling=0.5,
        random_state=42
    ).generate(text)
    
    return wordcloud

@st.cache_resource
def _load_models():
    """Load sentiment analysis models"""
    try:
        hf_analyzer = pipeline("sentiment-analysis", 
                              model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        return hf_analyzer, True
    except Exception as e:
        st.warning(f"Advanced sentiment model not available, using VADER\n\nReason:\n{e}")
        return SentimentIntensityAnalyzer(), False

class NewsDataCollector:
    """Handles news data collection from various RSS sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_google_news_url(self, query, region='US', language='en', category=None):
        """Generate Google News RSS URL with parameters"""
        base_url = "https://news.google.com/rss"
        
        if category:
            url = f"{base_url}/headlines/section/topic/{category}?hl={language}&gl={region}&ceid={region}:{language}"
        elif query:
            encoded_query = requests.utils.quote(query)
            url = f"{base_url}/search?q={encoded_query}&hl={language}&gl={region}&ceid={region}:{language}"
        else:
            url = f"{base_url}?hl={language}&gl={region}&ceid={region}:{language}"
            
        return url

    def _create_cache_key(self, url, max_articles):
        """Create a consistent cache key for RSS requests"""
        return hashlib.md5(f"{url}_{max_articles}".encode()).hexdigest()
    
    def scrape_rss_feed(self, url, max_articles=50):
        """Scrape articles from RSS feed and sort by recency"""
        return _scrape_rss_feed(url, max_articles)
    
    def collect_news_data(self, query=None, region='US', category=None, max_articles=50):
        """Main method to collect news data"""
        url = self.get_google_news_url(query, region, category=category)
        return self.scrape_rss_feed(url, max_articles)

class SentimentAnalyzer:
    """Advanced sentiment analysis using multiple models"""
    
    def __init__(self):
        self._hf_analyzer, self._use_hf = _load_models()
        if not self._use_hf:
            self._vader = self._hf_analyzer

    def _get_hf_sentiment_label(self, text):
        """Convert Hugging Face model prediction to descriptive sentiment label"""
        return self._hf_analyzer(text)[0]["label"]

    def _get_vader_sentiment_label(self, compound_score):
        """Convert vader compound score to descriptive label using best practices"""
        if compound_score >= 0.05:
            return "positive"
        elif compound_score > -0.05:
            return "neutral"
        else:
            return "negative"
    
    def analyze_text(self, text):
        """Comprehensive sentiment analysis"""
        # Use cached functions instead of caching instance methods
        if self._use_hf:
            result = _analyze_sentiment_hf(text)
            if result:
                return {'sentiment_label': result}
        
        # Fallback to VADER
        result = _analyze_sentiment_vader(text)
        return {'sentiment_label': result}

class TextSummarizer:
    """Text summarization using Hugging Face transformers"""

    def __init__(self):
        self._available = True

    def summarize_headlines(self, headlines):  
        """Summarize a list of headlines"""
        if not headlines:
            return "Summarization not available"
    
        try:
            # Shuffle headlines to get random selection
            headlines_copy = headlines.copy()
            random.shuffle(headlines_copy)

            combined_text = ""
            for headline in headlines_copy:
                if len(combined_text) >= 1000:
                    break
                combined_text += headline.strip() + ". "
        
            combined_text = combined_text.strip()

            if len(combined_text) < 50:
                return "Insufficient text for summarization"

            # Limit input for summarizer
            if len(combined_text) > 1000:
                combined_text = combined_text[:1000]

            summary = _summarize_text(combined_text)
            return summary if summary else "Summarization error"

        except Exception as e:
            return f"Summarization error: {e}"

class DataVisualizer:
    """Advanced data visualization for insights"""
    
    def __init__(self):
        plt.style.use('seaborn-v0_8')
    
    def create_wordcloud(self, text_data, exclude_words=None, colormap='viridis'):
        """Generate customizable word cloud"""
        if exclude_words is None:
            exclude_words = set()
        
        # Convert to tuple for caching (sets aren't hashable)
        exclude_words_tuple = tuple(sorted(exclude_words))
        
        return _create_wordcloud_data(text_data, exclude_words_tuple, colormap)
    
    @st.cache_data
    def plot_sentiment_distribution(_self, sentiments_tuple):
        """Create sentiment distribution bar chart"""
        # Convert tuple back to list for Counter
        sentiments = list(sentiments_tuple)
        sentiment_counts = Counter(sentiments)
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(sentiment_counts.keys()),
                y=list(sentiment_counts.values()),
                marker_color=['#ff4444', '#ffffff', '#00aa00']
            )
        ])
        
        fig.update_layout(
            title="Sentiment Distribution",
            xaxis_title="Sentiment",
            yaxis_title="Count",
            template="plotly_white"
        )
        
        return fig

class DataExporter:
    """Handle data export in multiple formats"""
    
    @staticmethod
    def to_csv(df):
        """Export DataFrame to CSV"""
        return df.to_csv(index=False)
    
    @staticmethod
    def to_json(df):
        """Export DataFrame to JSON"""
        return df.to_json(orient='records', date_format='iso')
    
    @staticmethod
    def wordcloud_to_png(wordcloud):
        """Convert wordcloud to PNG bytes"""
        if wordcloud is None:
            return None
            
        img_buffer = BytesIO()
        wordcloud.to_image().save(img_buffer, format='PNG')
        return img_buffer.getvalue()
