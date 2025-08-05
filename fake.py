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
        pass # To remove
    else:
        # for article in articles:
            # print(f"- {article['title']}")
            # print(f"  Source: {article['source']}")
            # print(f"  Published: {article['published']}")
        pass # To remove
        
def main():
    collector = (get_analyzers()[0])
    articles = collector.collect_news_data("Andrew Tate")
    
    df = pd.DataFrame(articles)
    
    mask = df['title'].str.lower().str.contains('|'.join(['canadian']), na=False)
    df = df[mask]
    
    titles = df['title'].tolist()
    results_df = pd.DataFrame(process_sentiment_analysis(titles))
    print('\n\n\n\n\n')
    
    df = pd.concat([df, results_df], axis=1)
    
    for _, row in df.iterrows():
        sentiment_color = {
            'Positive': 'green', 
            'Neutral': 'gray',
            'Negative': 'red'
        }.get(row['sentiment_label'], 'gray')
        
        print(row['title'])
        print(row['source'])
        print(row['sentiment_label'])
    
        


if __name__ == "__main__":
    main()