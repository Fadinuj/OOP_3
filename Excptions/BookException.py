from Excptions.LibraryException import LibraryException


class BookException(LibraryException):
    """Base exception for book-related errors."""
    pass

class BookNotFoundException(BookException):
    """Raised when a book is not found."""
    def __init__(self, title):
        super().__init__(f"Book '{title}' not found.")
