import streamlit as st
import re
from collections import Counter

# Visualization libraries
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.graph_objects as go

class DataVisualizer:
	"""Advanced data visualization for insights"""
	
	def __init__(self):
		plt.style.use('seaborn-v0_8')

	@st.cache_data
	def create_wordcloud(_self, text_data, exclude_words=None, colormap='viridis'):
		"""Generate customizable word cloud"""
		if exclude_words is None:
			exclude_words = set(['news', 'says', 'new', 'get', 'make', 'take'])
		
		# Convert set to sorted list for consistent caching
		exclude_words = sorted(list(exclude_words))
		
		# Clean and combine text
		text = ' '.join(text_data).lower()
		text = re.sub(r'[^\w\s]', ' ', text)
		
		# Remove common words
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
		
	@st.cache_data
	def plot_sentiment_distribution(_self, sentiments):
		"""Create sentiment distribution bar chart with fixed order and matching colors"""
		
		# Define the fixed sentiment order and corresponding colors
		sentiment_order = ['Positive', 'Neutral', 'Negative']
		color_map = {
			'Positive': '#00aa00',
			'Neutral': '#ffffff',
			'Negative': '#ff4444'
		}
		
		# Count sentiments in the data
		sentiment_counts = Counter(sentiments)
		
		# Build y-values based on fixed order, using 0 if a sentiment is missing
		y_values = [sentiment_counts.get(sentiment, 0) for sentiment in sentiment_order]
		colors = [color_map[sentiment] for sentiment in sentiment_order]
		
		# Create bar chart with consistent order and color
		fig = go.Figure(data=[
			go.Bar(
				x=sentiment_order,
				y=y_values,
				marker_color=colors
			)
		])
		
		fig.update_layout(
			title="Sentiment Distribution",
			xaxis_title="Sentiment",
			yaxis_title="Count",
			template="plotly_white"
		)
		
		return fig