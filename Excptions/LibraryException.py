class LibraryException(Exception):
    """
    Base class for all exceptions in the library system.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message
