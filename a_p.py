import streamlit as st
import pandas as pd
from datetime import datetime
import re
from collections import Counter
import matplotlib.pyplot as plt
from utils import get_analyzers, process_sentiment_analysis, generate_keyword_analysis

"""
Main function for the NewsSpeed application.

Sets up the Streamlit interface, collects and filters news articles,
performs sentiment and keyword analysis, generates visualizations,
and provides data export options.
"""
def main():
	"""Main Streamlit application"""
	
	# Page configuration
	st.set_page_config(
		page_title="NewsSpeed",
		page_icon="🌐",
		layout="wide",
		initial_sidebar_state="expanded"
	)
	
	# Styling
	st.markdown("""
	<style>
	.main-header {
		text-align: center;
		padding: 2rem 0;
		background: linear-gradient(110deg, #d7d7d7 0%, #2e2e2e 30%, #2e2e2e 50%, #000000 100%, #000000 100%);
		color: white;
		margin-bottom: 2rem;
		border-radius: 10px;
		transition: background 0.3s ease, filter 0.3s ease;
		position: relative;
		overflow: hidden;
	}
	
	.main-header:hover {
		filter: brightness(0.9);
	}
	
	.metric-card {
		background: #1e1e1e;
		padding: 1rem;
		border-radius: 10px;
		border-left: 4px solid #667eea;
		color: #ffffff;
		transition: background 0.3s ease;
	}

	.metric-card:hover {
		background: #2a2a2a;
	}

	</style>
	""", unsafe_allow_html=True)
	
	# Header
	st.markdown("""
	<div class="main-header">
		<h1>🌐 NewsSpeed</h1>
		<p>Advanced News Analysis & Sentiment Intelligence</p>
	</div>
	""", unsafe_allow_html=True)
	
	# Initialize components
	collector, analyzer, summarizer, visualizer = get_analyzers()
	
	# Sidebar configuration
	st.sidebar.header("🔧 Configuration")
	
	# Search parameters
	query = st.sidebar.text_input("Search Query", value="artificial intelligence", 
								 help="Enter keywords to search for")
	
	region = st.sidebar.selectbox("Region", 
								 options=['US', 'UK', 'CA', 'AU', 'NG', 'IN', 'DE', 'FR'],
								 help="Select geographical region")
	
	category_map = {
		'General': None,
		'Business': 'BUSINESS',
		'Technology': 'TECHNOLOGY', 
		'Health': 'HEALTH',
		'Science': 'SCIENCE',
		'Sports': 'SPORTS'
	}
	
	category = st.sidebar.selectbox("Category", options=list(category_map.keys()))
	
	max_articles = st.sidebar.slider("Max Articles", min_value=10, max_value=100, value=50)
	
	# Filtering options
	st.sidebar.header("🔍 Filtering")
	keyword_filter = st.sidebar.text_input("Filter by Keywords", 
										  help="Only display headlines containing these words; use commas to separate filter keywords")
	
	# Headlines
	st.sidebar.header("📰 Overview")
	max_headlines = st.sidebar.text_input("Max Headlines", value=50,
										  help="Input the maximum headlines to show; if input is invalid, this will default to the total articles found if the total articles are at most 50, else this will default to 50 articles; actual headlines displayed may be fewer than your chosen value")
	
	# Visualization options
	st.sidebar.header("🎨 Visualization")
	exclude_words = st.sidebar.text_area("Exclude Words from WordCloud and Top Keywords display", 
										value="news, says, new, get, make, with, this",
										help="Comma-separated words to exclude")
	
	colormap = st.sidebar.selectbox("WordCloud Color Scheme", 
								   options=['viridis', 'plasma', 'inferno', 'magma', 'Blues'])
	
	# Main content
	if st.sidebar.button("🚀 Analyze News", type="primary"):
		
		with st.spinner("Collecting news data..."):
			# Collect news data
			articles = collector.collect_news_data(
				query=query if query else None,
				region=region,
				category=category_map[category],
				max_articles=max_articles
			)
		
		if not articles:
			st.error("No articles found. Try adjusting your search parameters.")
			return
		
		# Convert to DataFrame
		df = pd.DataFrame(articles)
		
		# Apply keyword filtering
		if keyword_filter:
			keywords = [k.strip().lower() for k in keyword_filter.split(',')]
			mask = df['title'].str.lower().str.contains('|'.join(keywords), na=False)
			df = df[mask]
		
		if df.empty:
			st.warning("No articles match your filter criteria.")
			return
		
		# Perform sentiment analysis
		with st.spinner("Analyzing sentiment..."):
			titles = df['title'].tolist()
			sentiment_results = process_sentiment_analysis(titles)
	
			# Show visual progress
			progress_bar = st.progress(0)
			for idx in range(len(titles)):
				progress_bar.progress((idx + 1) / len(titles))
			progress_bar.empty()
		
		# Add sentiment data to DataFrame
		sentiment_df = pd.DataFrame(sentiment_results)
		df = pd.concat([df.reset_index(drop=True), sentiment_df.reset_index(drop=True)], axis=1)
		
		# Display metrics
		col1, col2, col3, col4, col5, col6 = st.columns(6)
		
		sentiment_counts = df['sentiment_label'].value_counts()
		total_articles = len(df)

		with col1:
			st.metric("Total Articles", total_articles)
		
		with col2:
			positive_pct = (sentiment_counts.get('positive', 0) / total_articles) * 100
			st.metric("Positive %", f"{positive_pct:.1f}%")

		with col3:
			neutral_pct = (sentiment_counts.get('neutral', 0) / total_articles) * 100
			st.metric("Neutral %", f"{neutral_pct:.1f}%")

		with col4:
			negative_pct = (sentiment_counts.get('negative', 0) / total_articles) * 100
			st.metric("Negative %", f"{negative_pct:.1f}%")
		
		if negative_pct > 0:
			with col5:
				ratio = positive_pct / negative_pct
				st.metric("Positive-to-Negative Ratio", f"{ratio:.2f}")
			
		with col6:
			top_source = df['source'].value_counts().index[0] if total_articles > 0 else "N/A"
			st.metric("Top Source", top_source)
		
		# Capitalize the first letter of each sentiment label (e.g., 'positive' → 'Positive') before proceeding
		df['sentiment_label'] = df['sentiment_label'].str.capitalize()
		
		# Tabs for different views
		tab1, tab2, tab3, tab4, tab5 = st.tabs(["📰 Overview", "🎨 Visualizations", "📝 Summary", "📋 Data", "💾 Export"])
		
		with tab1:
			# Convert input to integer if it's a digit-only string (e.g., "50"); otherwise, use total_articles as fallback
			max_headlines = int(max_headlines.strip()) if max_headlines.strip().isdigit() else total_articles
			displayable_headlines = min(max_headlines, total_articles)
			st.header(f"Headlines | {displayable_headlines}")
			
			# Display headlines with sentiment
			for _, row in df.iterrows():
				sentiment_color = {
					'Positive': 'green', 
					'Neutral': 'white',
					'Negative': 'red'
				}.get(row['sentiment_label'], 'gray')
				
				st.markdown(f"""
				<div class="metric-card">
					<h4>{row['title']}</h4>
					<p><strong>Source:</strong> {row['source']} | 
					<strong>Sentiment:</strong> <span style="color: {sentiment_color}">{row['sentiment_label']}</span></p>
				</div>
				""", unsafe_allow_html=True)
				st.markdown("<br>", unsafe_allow_html=True)
		
		with tab2:
			st.header("Data Visualizations")
			
			col, = st.columns(1)
			
			with col:
				# Sentiment distribution
				fig_sentiment = visualizer.plot_sentiment_distribution(df['sentiment_label'])
				st.plotly_chart(fig_sentiment, use_container_width=True)
			
			# Word cloud
			st.subheader("Word Cloud")
			
			global exclude_list
			exclude_list = [w.strip() for w in exclude_words.split(',') if w.strip()]
			wordcloud = visualizer.create_wordcloud(df['title'].tolist(), 
												   exclude_words=set(exclude_list),
												   colormap=colormap)
			
			if wordcloud:
				fig, ax = plt.subplots(figsize=(12, 6))
				ax.imshow(wordcloud, interpolation='bilinear')
				ax.axis('off')
				st.pyplot(fig)
			else:
				st.warning("Could not generate word cloud")
		
		with tab3:
			st.header("AI-Generated Summary")
			
			if summarizer.available:
				with st.spinner("Generating summary..."):
					summary = summarizer.summarize_headlines(df['title'].tolist())
					st.info(summary)
			else:
				st.warning("Summary feature not available")
			
			# Top keywords
			top_keywords = generate_keyword_analysis(df['title'].tolist())
			st.subheader(f"Top {len(top_keywords)} Keywords")
			
			keyword_df = pd.DataFrame(top_keywords, columns=['Keyword', 'Frequency'])
			st.dataframe(keyword_df, use_container_width=True)
		
		with tab4:
			st.header("Raw Data")
			
			# Display options
			show_columns = st.multiselect(
				"Select columns to display",
				options=df.columns.tolist(),
				default=['title', 'source', 'sentiment_label']
			)
			
			if show_columns:
				st.dataframe(df[show_columns], use_container_width=True)
		
		with tab5:
			st.header("Export Data")
			
			col1, col2, col3 = st.columns(3)
			
			file_name = f"newsspeed_data_{datetime.utcnow().strftime('%Y%m%d_%H%M')}-UTC"
			with col1:
				# CSV Export
				csv_data = DataExporter.to_csv(df)
				st.download_button(
					label="📄 Download CSV",
					data=csv_data,
					file_name=f"{file_name}.csv",
					mime="text/csv"
				)
			
			with col2:
				# JSON Export
				json_data = DataExporter.to_json(df)
				st.download_button(
					label="📋 Download JSON",
					data=json_data,
					file_name=f"{file_name}.json",
					mime="application/json"
				)
			
			with col3:
				# WordCloud PNG Export
				if 'wordcloud' in locals() and wordcloud:
					png_data = DataExporter.wordcloud_to_png(wordcloud)
					if png_data:
						st.download_button(
							label="🖼️ Download WordCloud",
							data=png_data,
							file_name=f"{file_name}.png",
							mime="image/png"
						)
	
	# Footer
	st.markdown("---")
	st.markdown("""
	<div style="text-align: center; color: #666;">
		<p>🌐 NewsSpeed - Built for tracking media narratives in real time</p>
		<p>Powered by Advanced NLP & Real-time Data Analysis</p>
	</div>
	""", unsafe_allow_html=True)

if __name__ == "__main__":
	main()