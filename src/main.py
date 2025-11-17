"""
Example usage of the News API classes.

Before running this code:
1. Get your API key from https://newsapi.org/register
2. Make sure to not push it to Github!
"""

from datetime import datetime, timedelta
import sys
sys.path.append('.')  # To allow imports from src
from src.search_news import SearchNews
from src.news_processor import NewsProcessor




def main() -> None:
    # Initialize the news searcher
    # Make sure you have your API key in 'api_key.txt'
    # print(os.path.exists('./key_stora.txt'))
    searcher = SearchNews('key_stora')
    
    # Initialize the processor
    processor = NewsProcessor()
    
    # Example 1: Get top headlines
    print("Getting top headlines...")
    headlines = searcher.get_top_headlines("technology")
    print(f"Found {len(headlines)} headlines")
    
    # Example 2: Convert to DataFrame
    print("\nConverting to DataFrame...")
    df = processor.to_df(headlines)
    print(df.head())
    
    # Example 3: Filter articles (only articles with authors)
    print("\nFiltering articles with authors...")
    df_with_authors = processor.to_df(
        headlines, 
        filter_func=lambda article: article.author is not None
    )
    print(f"Articles with authors: {len(df_with_authors)}")
    
    # Example 4: Sort by publication date
    print("\nSorting by publication date...")
    df_sorted = processor.to_df(
        headlines,
        sort_by=lambda article: article.published_at
    )
    print("Sorted DataFrame created")
    print(df_sorted.head())
    
    # Example 5: Plot word popularity
    print("\nPlotting word popularity...")
    processor.plot_word_popularity(headlines, "AI")
    
    # Example 6: Search everything for a specific term
    print("\nSearching everything for 'climate change'...")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    climate_articles = searcher.get_everything(yesterday, None, 'en', "climate change")
    print(f"Found {len(climate_articles)} articles about climate change")


if __name__ == "__main__":
    main()