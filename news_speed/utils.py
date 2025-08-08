from .collector import NewsDataCollector
from .analyzer import SentimentAnalyzer
from .summarizer import TextSummarizer
from .visualizer import DataVisualizer
import streamlit as st
import pandas as pd
from datetime import datetime
import re
from collections import Counter
import matplotlib.pyplot as plt

# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings('ignore')

@st.cache_resource
def get_analyzers():
	"""Initialize and cache the analyzer objects"""
	collector = NewsDataCollector()
	analyzer = SentimentAnalyzer()
	summarizer = TextSummarizer()
	visualizer = DataVisualizer()
	return collector, analyzer, summarizer, visualizer

@st.cache_data
def process_sentiment_analysis(titles):
	"""Cache sentiment analysis results"""
	_, analyzer, _, _ = get_analyzers()
	results = []
	for title in titles:
		sentiment = analyzer.analyze_text(title)
		results.append(sentiment)
	return results

@st.cache_data
def generate_keyword_analysis(titles):
	"""Cache keyword analysis"""
	all_text = ' '.join(titles).lower()
	words = re.findall(r'\b\w+\b', all_text)
	
	# Filter out excluded words
	if exclude_list:
		filtered_words = [w for w in words if len(w) > 3 and w not in set(exclude_list)]
	else:
		filtered_words = [w for w in words if len(w) > 3]
	
	word_freq = Counter(filtered_words)
	return word_freq.most_common(20)
