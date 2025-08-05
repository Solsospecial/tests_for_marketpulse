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
    
    for article in articles:
        del article['summary']
        del article['link']
    
    df = pd.DataFrame(articles)
    
    mask = df['title'].str.lower().str.contains('|'.join(['canadian']), na=False)
    df = df[mask]
    
    titles = df['title'].tolist()
    
    print('\n\n\n\n\n')
    
    results = process_sentiment_analysis(titles)
    
    print(f'Results: {results}')
    
    print('\n\n\n')
    
    results_df = pd.DataFrame(results)
    
    print('Results DF\n')
    
    print(results_df.values.tolist())
    
    print('\n\n\n')
    
    df = pd.concat([df.reset_index(drop=True), results_df.reset_index(drop=True)], axis=1)
    
    print('Concat DF\n')
    
    print(df.values.tolist())
    
    print('\n\n\n')

    for _, row in df.iterrows():
        sentiment_color = {
            'Positive': 'green', 
            'Neutral': 'gray',
            'Negative': 'red'
        }.get(row['sentiment_label'], 'gray')
        
        print(f"Title: {row['title']}")
        print(f"Source: {row['source']}")
        print(f"Sentiment: {row['sentiment_label']}")

if __name__ == "__main__":
    main()