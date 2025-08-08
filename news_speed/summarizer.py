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

@st.cache_resource
def load_summarizer():
	"""Load summarization model"""
	try:
		summarizer = pipeline("summarization", 
							model="facebook/bart-large-cnn",
							max_length=150, 
							min_length=30,
							do_sample=False)
		return summarizer, True
	except:
		try:
			# Fallback to smaller model
			summarizer = pipeline("summarization",
								model="sshleifer/distilbart-cnn-12-6",
								max_length=120,
								min_length=25)
			return summarizer, True
		except Exception as e:
			st.warning(f"Summarization model not available\n\nReason:\n{e}")
			return None, False

# Summarize news headlines
class TextSummarizer:
	"""Text summarization using Hugging Face transformers"""

	def __init__(self):
		self.summarizer, self.available = load_summarizer()

	@st.cache_data
	def summarize_headlines(_self, headlines):  
		"""Summarize a list of headlines"""
		if not _self.available or not headlines:
			return "Summarization not available"
	
		try:
			# Create a cache key based on headlines
			headlines_str = '|'.join(sorted(headlines))
			
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

			# Limit input for summarizer (most models prefer <1024 tokens ~ 1000–1500 characters)
			if len(combined_text) > 1000:
				combined_text = combined_text[:1000]

			summary = _self.summarizer(combined_text)[0]['summary_text']
			return summary

		except Exception as e:
			return f"Summarization error: {e}"