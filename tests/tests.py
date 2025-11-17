import unittest
import pandas as pd
from src.article import Article
from src.search_news import SearchNews
from src.news_processor import NewsProcessor
import os
from unittest.mock import patch, Mock
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing


class TestArticleAttributes(unittest.TestCase):
    """Tests for Article attributes and properties"""
    
    def test_all_attributes_with_values(self):
        article = Article(
            url="https://example.com/article",
            source="BBC News",
            author="John Doe",
            title="Test Article",
            description="Test description",
            published_at="2024-10-24T12:00:00Z",
            content="Full article content"
        )
        
        self.assertEqual(article.url, "https://example.com/article")
        self.assertEqual(article.source, "BBC News")
        self.assertEqual(article.author, "John Doe")
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.description, "Test description")
        self.assertEqual(article.published_at, "2024-10-24T12:00:00Z")
        self.assertEqual(article.content, "Full article content")
    
    def test_all_attributes_none(self):
        article = Article()
        
        self.assertIsNone(article.url)
        self.assertIsNone(article.source)
        self.assertIsNone(article.author)
        self.assertIsNone(article.title)
        self.assertIsNone(article.description)
        self.assertIsNone(article.published_at)
        self.assertIsNone(article.content)
    
    def test_partial_attributes(self):
        article = Article(
            title="Test Title",
            author="Test Author"
        )
        
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.author, "Test Author")
        self.assertIsNone(article.url)
        self.assertIsNone(article.source)


class TestArticleStr(unittest.TestCase):
    """Tests for Article __str__ method"""
    
    def test_str_with_all_values(self):
        article = Article(
            url="https://example.com",
            source="BBC News",
            author="John Doe",
            title="Test Article",
            description="Description",
            published_at="2024-10-24T12:00:00Z",
            content="Content"
        )
        
        result = str(article)
        self.assertEqual(result, "Test Article by John Doe on 2024-10-24T12:00:00Z")
    
    def test_str_with_none_values(self):
        article = Article(
            title="Test Title",
            author=None,
            published_at=None
        )
        
        result = str(article)
        self.assertEqual(result, "Test Title by None on None")
    
    def test_str_returns_string(self):
        article = Article()
        result = str(article)
        self.assertIsInstance(result, str)


class TestArticleRepr(unittest.TestCase):
    """Tests for Article __repr__ method"""
    
    def test_repr_with_all_values(self):
        article = Article(
            url="https://example.com",
            source="BBC News",
            author="John Doe",
            title="Test Article",
            description="Description",
            published_at="2024-10-24T12:00:00Z",
            content="Content"
        )
        
        result = repr(article)
        expected = "Article(title='Test Article', author='John Doe', source='BBC News', publishedAt='2024-10-24T12:00:00Z')"
        self.assertEqual(result, expected)
    
    def test_repr_with_none_values(self):
        article = Article()
        
        result = repr(article)
        expected = "Article(title='None', author='None', source='None', publishedAt='None')"
        self.assertEqual(result, expected)
    
    def test_repr_format(self):
        article = Article(title="Title", author="Author", source="Source", published_at="2024-10-24")
        result = repr(article)
        
        self.assertIn("Article(", result)
        self.assertIn("title='Title'", result)
        self.assertIn("author='Author'", result)
        self.assertIn("source='Source'", result)
        self.assertIn("publishedAt='2024-10-24'", result)


class TestSearchNewsConstructor(unittest.TestCase):
    """Tests for SearchNews constructor"""
    
    def setUp(self):
        # Create test API key file
        self.test_key_file = 'test_api_key.txt'
        with open(self.test_key_file, 'w') as f:
            f.write('test_api_key_12345')
    
    def tearDown(self):
        # Clean up test file
        if os.path.exists(self.test_key_file):
            os.remove(self.test_key_file)
    
    def test_constructor_reads_file(self):
        searcher = SearchNews(self.test_key_file)
        self.assertIsNotNone(searcher)
    
    def test_constructor_with_whitespace(self):
        whitespace_file = 'test_whitespace.txt'
        with open(whitespace_file, 'w') as f:
            f.write('  test_key_with_spaces  \n')
        
        searcher = SearchNews(whitespace_file)
        self.assertIsNotNone(searcher)
        
        os.remove(whitespace_file)
    
    def test_constructor_with_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            SearchNews('nonexistent_file.txt')
    
    def test_constructor_with_empty_file(self):
        empty_file = 'test_empty.txt'
        with open(empty_file, 'w') as f:
            f.write('')
        
        searcher = SearchNews(empty_file)
        self.assertIsNotNone(searcher)
        
        os.remove(empty_file)


class TestNewsProcessorToDf(unittest.TestCase):
    """Tests for NewsProcessor to_df() method"""
    
    def setUp(self):
        self.processor = NewsProcessor()
        self.articles = [
            Article(
                url="https://example.com/1",
                source="BBC",
                author="Author 1",
                title="Article 1",
                description="Description 1",
                published_at="2024-10-24T12:00:00Z",
                content="Content 1"
            ),
            Article(
                url="https://example.com/2",
                source="CNN",
                author="Author 2",
                title="Article 2",
                description="Description 2",
                published_at="2024-10-23T12:00:00Z",
                content="Content 2"
            ),
            Article(
                url="https://example.com/3",
                source="BBC",
                author="Author 3",
                title="Article 3",
                description="Description 3",
                published_at="2024-10-22T12:00:00Z",
                content="Content 3"
            )
        ]
    
    def test_basic_conversion(self):
        df = self.processor.to_df(self.articles)
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertListEqual(list(df.columns), 
                           ['url', 'source', 'author', 'title', 'description', 'published_at', 'content'])
    
    def test_dataframe_content(self):
        df = self.processor.to_df(self.articles)
        
        self.assertEqual(df.iloc[0]['title'], "Article 1")
        self.assertEqual(df.iloc[1]['author'], "Author 2")
        self.assertEqual(df.iloc[2]['source'], "BBC")
    
    def test_empty_list(self):
        df = self.processor.to_df([])
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 0)
    
    def test_filter_func(self):
        df = self.processor.to_df(
            self.articles,
            filter_func=lambda a: a.source == "BBC"
        )
        
        self.assertEqual(len(df), 2)
        self.assertTrue(all(df['source'] == 'BBC'))
    
    def test_filter_func_no_matches(self):
        df = self.processor.to_df(
            self.articles,
            filter_func=lambda a: a.source == "FOX"
        )
        
        self.assertEqual(len(df), 0)
    
    def test_sort_by_published_at(self):
        df = self.processor.to_df(
            self.articles,
            sort_by=lambda a: a.published_at
        )
        
        dates = df['published_at'].tolist()
        self.assertEqual(dates[0], "2024-10-22T12:00:00Z")
        self.assertEqual(dates[1], "2024-10-23T12:00:00Z")
        self.assertEqual(dates[2], "2024-10-24T12:00:00Z")
    
    def test_sort_by_title(self):
        df = self.processor.to_df(
            self.articles,
            sort_by=lambda a: a.title
        )
        
        titles = df['title'].tolist()
        self.assertEqual(titles, ["Article 1", "Article 2", "Article 3"])
    
    def test_filter_and_sort_combined(self):
        df = self.processor.to_df(
            self.articles,
            filter_func=lambda a: a.source == "BBC",
            sort_by=lambda a: a.published_at
        )
        
        self.assertEqual(len(df), 2)
        self.assertTrue(all(df['source'] == 'BBC'))
        dates = df['published_at'].tolist()
        self.assertEqual(dates[0], "2024-10-22T12:00:00Z")
        self.assertEqual(dates[1], "2024-10-24T12:00:00Z")
    
    def test_with_none_values(self):
        articles_with_none = [
            Article(
                url="https://example.com",
                source=None,
                author=None,
                title="Title",
                description=None,
                published_at=None,
                content=None
            )
        ]
        
        df = self.processor.to_df(articles_with_none)
        
        self.assertEqual(len(df), 1)
        self.assertIsNone(df.iloc[0]['author'])
        self.assertIsNone(df.iloc[0]['source'])


class TestSearchNewsGetTopHeadlines(unittest.TestCase):
    """Tests for SearchNews get_top_headlines method"""
    
    def setUp(self):
        # Create test API key file
        self.test_key_file = 'test_api_key.txt'
        with open(self.test_key_file, 'w') as f:
            f.write('test_api_key')
        self.searcher = SearchNews(self.test_key_file)
    
    def tearDown(self):
        if os.path.exists(self.test_key_file):
            os.remove(self.test_key_file)
    
    @patch('requests.get')
    def test_successful_request(self, mock_get):
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'articles': [
                {
                    'url': 'https://example.com/1',
                    'source': {'name': 'BBC'},
                    'author': 'Author 1',
                    'title': 'Title 1',
                    'description': 'Description 1',
                    'publishedAt': '2024-10-24T12:00:00Z',
                    'content': 'Content 1'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        articles = self.searcher.get_top_headlines()
        
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'Title 1')
        self.assertEqual(articles[0].author, 'Author 1')
    
    @patch('requests.get')
    def test_with_search_terms(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'articles': []}
        mock_get.return_value = mock_response
        
        self.searcher.get_top_headlines("bitcoin", "crypto")
        
        # Verify the API was called with correct params
        call_args = mock_get.call_args
        self.assertIn('q', call_args[1]['params'])
        self.assertEqual(call_args[1]['params']['q'], 'bitcoin crypto')
    
    @patch('requests.get')
    def test_with_domains(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'articles': []}
        mock_get.return_value = mock_response
        
        self.searcher.get_top_headlines(domains=['bbc.co.uk', 'cnn.com'])
        
        call_args = mock_get.call_args
        self.assertIn('domains', call_args[1]['params'])
        self.assertEqual(call_args[1]['params']['domains'], 'bbc.co.uk,cnn.com')
    
    @patch('requests.get')
    def test_error_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        articles = self.searcher.get_top_headlines()
        
        self.assertEqual(articles, [])


class TestSearchNewsGetEverything(unittest.TestCase):
    """Tests for SearchNews get_everything method"""
    
    def setUp(self):
        self.test_key_file = 'test_api_key.txt'
        with open(self.test_key_file, 'w') as f:
            f.write('test_api_key')
        self.searcher = SearchNews(self.test_key_file)
    
    def tearDown(self):
        if os.path.exists(self.test_key_file):
            os.remove(self.test_key_file)
    
    @patch('requests.get')
    def test_successful_request(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'articles': [
                {
                    'url': 'https://example.com/1',
                    'source': {'name': 'BBC'},
                    'author': 'Author 1',
                    'title': 'Title 1',
                    'description': 'Description 1',
                    'publishedAt': '2024-10-24T12:00:00Z',
                    'content': 'Content 1'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        articles = self.searcher.get_everything()
        
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'Title 1')


class TestNewsProcessorPlotWordPopularity(unittest.TestCase):
    """Tests for NewsProcessor plot_word_popularity method"""
    
    def setUp(self):
        self.processor = NewsProcessor()
        self.articles = [
            Article(
                title="Bitcoin rises today",
                published_at="2024-10-24T12:00:00Z"
            ),
            Article(
                title="Bitcoin falls yesterday",
                published_at="2024-10-24T13:00:00Z"
            ),
            Article(
                title="Stock market update",
                published_at="2024-10-23T12:00:00Z"
            ),
            Article(
                title="Bitcoin news",
                published_at="2024-10-23T14:00:00Z"
            )
        ]
    
    @patch('matplotlib.pyplot.show')
    def test_plot_creates_without_error(self, mock_show):
        # Should not raise any exceptions
        self.processor.plot_word_popularity(self.articles, "bitcoin")
        mock_show.assert_called_once()
    
    @patch('matplotlib.pyplot.show')
    def test_plot_with_no_matches(self, mock_show):
        self.processor.plot_word_popularity(self.articles, "ethereum")
        mock_show.assert_called_once()
    
    @patch('matplotlib.pyplot.show')
    def test_plot_with_empty_articles(self, mock_show):
        self.processor.plot_word_popularity([], "bitcoin")
        mock_show.assert_called_once()


if __name__ == '__main__':
    unittest.main()