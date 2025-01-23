from abc import ABC, abstractmethod

from Backend.Logger import Logger


# Abstract base class for search strategies
class Strategy_Search(ABC):
    @abstractmethod
    def search(self, keyword):
        """Search for books based on the keyword."""
        pass

# Concrete search strategy: Search by Title
class SearchByTitle(Strategy_Search):
    def search(self, keyword,books):
        keyword = keyword.strip().lower()  # Strip whitespace and convert to lowercase
        # Filter books based on the keyword appearing in any attribute
        matching_books = [
            book for book in books
            if keyword in book.title.lower()
        ]

        return matching_books

# Concrete search strategy: Search by Author
class SearchByAuthor(Strategy_Search):
    def search(self, keyword, books):
        keyword = keyword.strip().lower()  # Strip whitespace and convert to lowercase
        # Filter books based on the keyword appearing in any attribute
        matching_books = [
            book for book in books
            if keyword in book.author.lower()
        ]

        return matching_books
# Concrete search strategy: Search by Genre
class SearchByGenre(Strategy_Search):
    def search(self, keyword, books):
        keyword = keyword.strip().lower()  # Strip whitespace and convert to lowercase
        # Filter books based on the keyword appearing in any attribute
        matching_books = [
            book for book in books
            if keyword in book.genre.lower()
        ]

        return matching_books

# Concrete search strategy: Search by Year
class SearchByYear(Strategy_Search):
    def search(self, keyword, books):
        try:
            year = int(keyword.strip())  # Convert keyword to integer
            # Filter books based on the year
            matching_books = [
                book for book in books
                if book.year == year  # Compare the book's year directly
            ]
            return matching_books
        except ValueError:
            # If the keyword is not a valid integer, return an empty list
            return []

# Context class for managing search strategies
class SearchContext:
    def __init__(self, strategy: Strategy_Search):
        self.strategy = strategy

    def set_strategy(self, strategy: Strategy_Search):
        """Set a new search strategy."""
        self.strategy = strategy

    def search(self, keyword, field ,books):
        """Perform search using the current strategy."""
        if field == "Title":
            titleSearch = SearchByTitle()
            Logger.log_info(f"Search book by name {keyword} completed successfully")
            return titleSearch.search(keyword,books)
        elif field == "Author":
            titleSearch = SearchByAuthor()
            Logger.log_info(f"Search book by name author {keyword} completed successfully")
            return titleSearch.search(keyword, books)
        elif field == "Genre":
            titleSearch = SearchByGenre()
            Logger.log_info(f"Search book by name Genre completed {keyword} successfully")
            return titleSearch.search(keyword, books)
        elif field == "Year":
            titleSearch = SearchByYear()
            Logger.log_info(f"Search book  by year {keyword} completed successfully")
            return titleSearch.search(keyword, books)


