# 🌐 NewsSpeed

**Real-Time News Analysis & Sentiment Intelligence Platform**  
*Track narratives, measure sentiment, extract insights — instantly.*

---

## 📌 Overview

**NewsSpeed** is a fully interactive, Streamlit-powered web application that:
- Collects the latest headlines from **Google News RSS feeds** (query, region, category).
- Applies **sentiment analysis** using advanced NLP models (Hugging Face Transformers, VADER fallback).
- Generates **word clouds**, **keyword frequency analysis**, and **sentiment distribution visualizations**.
- Summarizes multiple headlines into a concise **AI-generated summary**.
- Exports processed results in **CSV**, **JSON**, or **PNG** formats.

Built for:
- **Business intelligence teams**
- **Media & PR analysts**
- **Finance & investment research**
- **Technology & industrial monitoring**
- And anyone tracking topics in real time

---

## ✨ Features

- **News Collection**  
  - Region & category-specific news sourcing from Google News RSS feeds  
  - Search keyword–driven article retrieval  
  - Configurable max articles per run  

- **Sentiment Analysis**  
  - Uses Hugging Face’s `cardiffnlp/twitter-roberta-base-sentiment-latest`  
  - Falls back to VADER if transformer models are unavailable  
  - Classifies into **Positive**, **Neutral**, **Negative**  

- **Keyword Intelligence**  
  - Extracts most frequent keywords from headlines  
  - Exclusion list for ignoring stopwords or domain-specific noise  
  - Supports both visualization and tabular format  

- **Visualization**  
  - Interactive **sentiment distribution chart** (Plotly)  
  - Customizable **word cloud** (matplotlib + wordcloud library)  
  - Top keyword list with frequencies  

- **AI-Powered Summarization**  
  - Uses `facebook/bart-large-cnn` or fallback `distilbart` summarizer  
  - Generates a clear, concise narrative from multiple headlines  

- **Data Export**  
  - Download processed dataset in **CSV** or **JSON** format  
  - Save generated word cloud as a **PNG image**  

- **Streamlit UI Enhancements**  
  - Sidebar-driven configuration  
  - Multi-tab results: Overview, Visualizations, Summary, Data, Export  
  - Responsive layout with styled metric cards  

---

## 📂 Project Structure
```bash
root/
├── app.py                     # Main Streamlit application entry point
├── requirements.txt           # Python dependencies
└── news_speed/
├── init.py             # Package initializer
├── utils.py                # Helper functions & global analyzers
├── collector.py            # Google News RSS scraping & parsing
├── analyzer.py             # Sentiment analysis models
├── summarizer.py           # AI headline summarization
├── visualizer.py           # Sentiment chart & word cloud generation
└── exporter.py             # CSV, JSON, PNG export utilities
```

---

## 🚀 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/newsspeed.git
cd newsspeed
```
2️⃣ Create & activate a virtual environment (recommended)
```bash
# Windows
python -m venv venv

# macOS / Linux
venv\Scripts\activate
source venv/bin/activate
```
3️⃣ Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
___

## ▶️ Usage

Run the Streamlit app:
```bash
streamlit run app.py
```
By default, Streamlit will launch a local server at:

http://localhost:850

___

## ⚙️ Configuration (via Sidebar)
	•	Search Query – Keywords to find in headlines
	•	Region – Geographical focus (US, UK, CA, AU, NG, IN, DE, FR)
	•	Category – General, Business, Technology, Health, Science, Sports
	•	Max Articles – Limit on fetched articles (10–100)
	•	Filter by Keywords – Comma-separated list to filter results
	•	Max Headlines – Limit displayed headlines in Overview tab
	•	Exclude Words – Ignore certain words in word cloud / top keywords
	•	WordCloud Color Scheme – Choose visual palette

___

## 📊 Output

Overview Tab
	•	Headlines with source and sentiment label
	•	Sentiment metrics: Total articles, % Positive/Neutral/Negative, Ratio, Top source

Visualizations Tab
	•	Sentiment distribution bar chart
	•	Word cloud of most common headline words

Summary Tab
	•	AI-generated narrative
	•	Top keywords with frequency table

Data Tab
	•	Filterable raw dataset with selectable columns

Export Tab
	•	CSV, JSON, PNG downloads

___

## 🧠 Technology Stack
	•	Frontend/UI – Streamlit
	•	Data Handling – Pandas
	•	News Source – Google News RSS (via feedparser & requests)
	•	Sentiment Analysis – Hugging Face Transformers, VADER Sentiment
	•	Summarization – Hugging Face Transformers (BART models)
	•	Visualization – Plotly, Matplotlib, WordCloud
	•	Export – CSV, JSON, PNG (word cloud image)

___

## ⚠️ Notes & Limitations
	•	Model Downloads – First run will download large Hugging Face models; ensure internet access.
	•	Rate Limits – Google News RSS scraping may be subject to request frequency limitations.
	•	Summarization Length – Summaries are optimized for ~1000 characters of headline text.
	•	Caching – Streamlit caching (@st.cache_data / @st.cache_resource) is used to improve performance.

___

## 📜 License

This project is licensed under the MIT License.

___

## 📬 Contact

### For inquiries or feature requests:

Email: # Placeholder
LinkedIn: # Placeholder