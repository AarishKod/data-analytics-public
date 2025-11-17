import requests
from typing import Optional, List, Dict, Any
from src.article import Article
import os



class SearchNews:
    """
    Class to interact with the News API and retrieve news articles.
    """

    def __init__(self, api_key: str):
        """
        Initialize SearchNews by reading API key from file.

        Args:
            api_key_file: Path to file containing the API key
        """
        self.__api_key = open(api_key, 'r').read().strip()

    def get_top_headlines(self, date: Optional[str] = None, domains: Optional[List[str]] = None, language: Optional[str] = None, *terms: str) -> List[Article]:
        """
        Get top headlines from the News API.

        Args:
            date: Optional date filter (YYYY-MM-DD format)
            domain: Optional domain filter (e.g., 'bbc.co.uk')
            language: Optional language filter (e.g., 'en')
            *terms: Variable number of search terms

        Returns:
            List of Article objects
        """

        # TODO: Implement API call to /top-headlines endpoint
        params = {
            'apiKey': self.__api_key,
        }

        if terms:
            params['q'] = ' '.join(terms)
        if date:
            params['from'] = date
        if domains:
            params["domains"] = ",".join(domains)
        if language:
            params["language"] = language

        list_of_articles: List[Article] = []

        response = requests.get("https://newsapi.org/v2/top-headlines", params=params)

        if response.status_code == 200:
            data = response.json()
            for article in data["articles"]:
                list_of_articles.append(Article(url=article.get("url"), source=article.get("source", {}).get("name"), author=article.get("author"), title=article.get("title"), description=article.get("description"), published_at=article.get("publishedAt"), content=article.get("content")))
        else:
            print(f"Error: {response.status_code}")
            return []
        
        return list_of_articles


    def get_everything(
        self,
        date: Optional[str] = None,
        domains: Optional[List[str]] = None,
        language: Optional[str] = None,
        *terms: str
    ) -> List[Article]:
        """
        Get everything from the News API.

        Args:
            date: Optional date filter (YYYY-MM-DD format)
            domain: Optional domain filter (e.g., 'bbc.co.uk')
            language: Optional language filter (e.g., 'en')
            *terms: Variable number of search terms

        Returns:
            List of Article objects
        """

        params = {
            'apiKey': self.__api_key,
        }

        if terms:
            params["q"] = ' '.join(terms)
        if date:
            params['from'] = date
        if domains:
            params["domains"] = ",".join(domains)
        if language:
            params["language"] = language
        # TODO: Implement API call to /everything endpoint
        list_of_articles: List[Article] = []

        response = requests.get("https://newsapi.org/v2/everything", params=params)

        if response.status_code == 200:
            data = response.json()
            for article in data["articles"]:
                list_of_articles.append(Article(url=article.get("url"), source=article.get("source", {}).get("name"), author=article.get("author"), title=article.get("title"), description=article.get("description"), published_at=article.get("publishedAt"), content=article.get("content")))
        else:
            print(f"Error: {response.status_code}")
            return []
        
        return list_of_articles

    def _make_request(self, endpoint: str, params: Dict[str, str]) -> Any:
        """
        Helper method to make API requests.

        Args:
            endpoint: API endpoint (e.g., 'top-headlines')
            params: Query parameters for the request

        Returns:
            Dictionary of JSON response
        """
        # TODO: Implement helper method for making API requests


        response = requests.get(f"https://newsapi.org/v2/{endpoint}", params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return {}
        return response.json() # ts is a dictionary ()
        

    def _create_articles_from_response(self, response_data: Dict[str, Any]) -> List[Article]:
        """
        Helper method to create Article objects from API response.

        Args:
            response_data: JSON response from API

        Returns:
            List of Article objects
        """
        # TODO: Parse the 'articles' field from response and create Article objects
        list_of_articles: List[Article] = []
        for article in response_data["articles"]:
                list_of_articles.append(Article(url=article.get("url"), source=article.get("source", {}).get("name"), author=article.get("author"), title=article.get("title"), description=article.get("description"), published_at=article.get("publishedAt"), content=article.get("content")))

        return list_of_articles
        
