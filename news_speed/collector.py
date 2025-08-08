import streamlit as st
import feedparser
import requests
from datetime import datetime
from dateutil import parser
import hashlib

# Collect news data from the Google News RSS feed
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
		
		# Prioritize query over category
		if query:
			encoded_query = requests.utils.quote(query)
			url = f"{base_url}/search?q={encoded_query}&hl={language}&gl={region}&ceid={region}:{language}"
		elif category:
			url = f"{base_url}/headlines/section/topic/{category}?hl={language}&gl={region}&ceid={region}:{language}"
		else:
			url = f"{base_url}?hl={language}&gl={region}&ceid={region}:{language}"
			
		return url

	def _create_cache_key(self, url, max_articles):
		"""Create a consistent cache key for RSS requests"""
		return hashlib.md5(f"{url}_{max_articles}".encode()).hexdigest()
	
	@st.cache_data(ttl=300)  # Cache for 5 minutes
	def scrape_rss_feed(_self, url, max_articles=50):
		"""Scrape articles from RSS feed and sort by recency"""
		try:
			feed = feedparser.parse(url)
			articles = []
			
			for entry in feed.entries:
				# Parse the published date for sorting
				published_date = None
				if hasattr(entry, 'published_parsed') and entry.published_parsed:
					try:
						published_date = datetime(*entry.published_parsed[:6])
					except:
						pass
			
				# Fallback: try to parse published string
				if not published_date and entry.get('published'):
					try:
						published_date = parser.parse(entry.published)
					except:
						pass
				
				raw_title = entry.get('title', '') # Get title from feed entry
				# Clean the title by removing trailing ' - Source Name'
				clean_title = raw_title.rsplit(' - ', 1)[0] if ' - ' in raw_title else raw_title

				article = {
					'title': clean_title,
					'link': entry.get('link', ''),
					'published': entry.get('published', ''),
					'published_date': published_date,  # Helper field for sorting
					'summary': entry.get('summary', ''),
					'source': entry.get('source', {}).get('title', 'Unknown')
				}
				articles.append(article)
				
			# Sort by published date (most recent first)
			articles.sort(key=lambda x: x['published_date'] or datetime.min, reverse=True)
		
			# Remove helper field and return limited results
			for article in articles:
				del article['published_date']
		
			return articles[:max_articles]

		except Exception as e:
			st.error(f"Error scraping feed: {str(e)}")
			return []
	
	@st.cache_data(ttl=300)  # Cache for 5 minutes
	def collect_news_data(_self, query=None, region='US', category=None, max_articles=50):
		"""Main method to collect news data"""
		url = _self.get_google_news_url(query, region, category=category)
		return _self.scrape_rss_feed(url, max_articles)