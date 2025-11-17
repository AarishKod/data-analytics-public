import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Callable, Optional, Any
import datetime
from src.article import Article


class NewsProcessor:
    """
    Class to process and visualize news articles data.
    """

    def to_df(self, articles: List[Article],
              sort_by: Optional[Callable[[Article], Any]] = None,
              filter_func: Optional[Callable[[Article], bool]] = None
    ) -> pd.DataFrame:
        """
        Convert list of Article objects to a Pandas DataFrame.

        Args:
            articles: List of Article objects
            sort_by: Optional function to sort rows by
            filter_func: Optional function to filter rows (include rows where function returns True)

        Returns:
            Pandas DataFrame with articles data
        """
        # TODO: Convert Article objects to DataFrame
        # Each Article attribute will be a column
        # Each article will be a row

        # TODO: Apply filtering if filter_func is provided
        if filter_func is not None:
            articles = [article for article in articles if filter_func(article)]

        # TODO: Apply sorting if sort_by is provided
        if sort_by is not None:
            articles = sorted(articles, key=sort_by)

        data: List[Dict[str, Any]] = []
        for article in articles:
            data.append({
                'url': article.url,
                'source': article.source,
                'author': article.author,
                'title': article.title,
                'description': article.description,
                'published_at': article.published_at,
                'content': article.content
            })
        
        df = pd.DataFrame(data)
        return df


    def plot_word_popularity(self, articles: List[Article], search_term: str) -> None:
        """
        Plot the frequency of a search term in article titles over time.

        Args:
            articles: List of Article objects
            search_term: The term to search for in titles
        """
        # TODO:
        # 1. Extract dates and titles from articles
        list_of_dict_of_date_title: List[Dict[str, str]] = []
        for article in articles:
            if article.published_at is not None and article.title is not None:
                list_of_dict_of_date_title.append({
                    "date": article.published_at,
                    "title": article.title
                })
        # 2. Count occurrences of search_term in titles for each date
        date_counts: Dict[str, int] = {}
        for info_set in list_of_dict_of_date_title:
            if search_term.lower() in info_set["title"].lower():
                date_counts[info_set["date"].split('T')[0]] += 1
        # 3. Create a plot with dates on x-axis and frequency on y-axis
        sorted_dates = sorted(date_counts.keys())
        frequencies: List[int] = [date_counts[date] for date in sorted_dates]

        # 4. Display the plot
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_dates, frequencies, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Frequency')
        plt.title(f'Frequency of "{search_term}" in Article Titles Over Time')
        plt.xticks(rotation=45)  # Rotate x-axis labels for readability
        plt.tight_layout()  # Adjust layout to prevent label cutoff
        plt.show()


    
    # TODO:
    def _extract_date_from_published_at(self, published_at: Optional[str]) -> Optional[datetime.date]:
        """
        Helper method to extract date from publishedAt timestamp.

        Args:
            published_at: ISO format timestamp string (e.g., '2023-10-01T12:34:56Z')

        Returns:
            Date string in YYYY-MM-DD format, or None if input is None
        """
        # TODO: Parse ISO timestamp and return just the date part
        pass

    def _count_word_in_title(self, title: str, search_term: str) -> int:
        """
        Helper method to count occurrences of search term in title.

        Args:
            title: Article title
            search_term: Term to search for

        Returns:
            Number of occurrences (case-insensitive)
        """
        # TODO: Count occurrences of search_term in title (case-insensitive)
        pass
