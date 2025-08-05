from utils import NewsDataCollector

def main():
    collector = NewsDataCollector()
    news = collector.collect_news_data("Andrew Tate")

    articles = [
        i for i in news
        if 'canadian' in i['title'].lower()]

    if not articles:
        print("No articles found with 'canadian' in title or summary.")
    else:
        for article in articles:
            print(f"- {article['title']}")
            print(f"  Source: {article['source']}")
            print(f"  Published: {article['published']}")

if __name__ == "__main__":
    main()