import unittest
from Strategy_Search import SearchByTitle, SearchByAuthor, SearchByGenre, SearchByYear

class TestStrategySearch(unittest.TestCase):
    def setUp(self):
        self.books = [
            {"title": "Book One", "author": "Author One", "genre": "Fiction", "year": 2020},
            {"title": "Book Two", "author": "Author Two", "genre": "Non-Fiction", "year": 2021},
        ]

    def test_search_by_title(self):
        strategy = SearchByTitle()
        results = strategy.search("Book One", self.books)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Book One")

    def test_search_by_author(self):
        strategy = SearchByAuthor()
        results = strategy.search("Author Two", self.books)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["author"], "Author Two")

    def test_search_by_year(self):
        strategy = SearchByYear()
        results = strategy.search("2021", self.books)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["year"], 2021)
