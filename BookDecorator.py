class BookDecorator:
    def __init__(self, book):
        """
        Initialize the decorator with a book object.
        :param book: An instance of the Book class.
        """
        self.book = book

    def display_details(self):
        """Call the base book's display_details method."""
        return self.book.display_details()
