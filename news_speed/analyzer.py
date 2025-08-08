import streamlit as st
import feedparser
import requests
import random
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

@st.cache_resource
def load_models():
	"""Load sentiment analysis models"""
	try:
		hf_analyzer = pipeline("sentiment-analysis", 
								model="cardiffnlp/twitter-roberta-base-sentiment-latest")
		return hf_analyzer, True
	except Exception as e:
		st.warning(f"Advanced sentiment model not available, using VADER\n\nReason:\n{e}")
		return SentimentIntensityAnalyzer(), False

class SentimentAnalyzer:
	"""Advanced sentiment analysis using multiple models"""
	
	def __init__(self):
		self.hf_analyzer, self.use_hf = load_models()
		if not self.use_hf:
			self.vader = self.hf_analyzer

	def get_hf_sentiment_label(self, text):
		"""Convert Hugging Face model prediction to descriptive sentiment label"""
		return self.hf_analyzer(text)[0]["label"]

	def get_vader_sentiment_label(self, compound_score):
		"""Convert vader compound score to descriptive label using best practices"""
		if compound_score >= 0.05:
			return "positive"
		elif compound_score > -0.05:
			return "neutral"
		else:
			return "negative"
	
	@st.cache_data
	def analyze_text(_self, text):
		"""Comprehensive sentiment analysis"""
		# Use Hugging Face if available
		if _self.use_hf:
			try:
				return {'sentiment_label': _self.get_hf_sentiment_label(text)}
			except:
				pass
		# Else, use VADER
		return {'sentiment_label': _self.get_vader_sentiment_label(_self.vader.polarity_scores(text)['compound'])}