from app import get_analyzers, process_sentiment_analysis
import pandas as pd

def sub_main():
    collector = (get_analyzers()[0])
    news = collector.collect_news_data("Andrew Tate")

    articles = [
        i for i in news
        if 'canadian' in i['title'].lower()]

    if not articles:
        # print("No articles found with 'canadian' in title or summary.")
    else:
        for article in articles:
            # print(f"- {article['title']}")
            # print(f"  Source: {article['source']}")
            # print(f"  Published: {article['published']}")

def main():
    collector = (get_analyzers()[0])
    news = collector.collect_news_data("Andrew Tate")
    
    df = pd.DataFrame(articles)
    
    mask = df['title'].str.lower().str.contains('|'.join(['canadian']), na=False)
    df = df[mask]
    
    titles = df['title'].tolist()
    results = process_sentiment_analysis(titles)
    
    print(results)
        


if __name__ == "__main__":
    main()