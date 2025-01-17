from Excptions.LibraryException import LibraryException


class UserException(LibraryException):
    """Base exception for user-related errors."""
    pass

class UserNotFoundException(UserException):
    """Raised when a user is not found."""
    def __init__(self, username):
        super().__init__(f"User '{username}' not found.")
