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
