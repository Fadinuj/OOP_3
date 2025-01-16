from abc import ABC, abstractmethod
from BookManager import BookManager

# Abstract base class for search strategies
class Strategy_Search(ABC):
    @abstractmethod
    def search(self, keyword):
        """Search for books based on the keyword."""
        pass

# Concrete search strategy: Search by Title
class SearchByTitle(Strategy_Search):
    def search(self, keyword):
        return [book for book in BookManager.books if keyword.lower() in book.title.lower()]

# Concrete search strategy: Search by Author
class SearchByAuthor(Strategy_Search):
    def search(self, keyword):
        return [book for book in BookManager.books if keyword.lower() in book.author.lower()]

# Concrete search strategy: Search by Genre
class SearchByGenre(Strategy_Search):
    def search(self, keyword):
        return [book for book in BookManager.books if keyword.lower() in book.genre.lower()]

# Concrete search strategy: Search by Year
class SearchByYear(Strategy_Search):
    def search(self, keyword):
        try:
            year = int(keyword)
            return [book for book in BookManager.books if book.year == year]
        except ValueError:
            return []  # Return empty list if the keyword is not a valid year

# Context class for managing search strategies
class SearchContext:
    def __init__(self, strategy: Strategy_Search):
        self.strategy = strategy

    def set_strategy(self, strategy: Strategy_Search):
        """Set a new search strategy."""
        self.strategy = strategy

    def search(self, keyword):
        """Perform search using the current strategy."""
        return self.strategy.search(keyword)
