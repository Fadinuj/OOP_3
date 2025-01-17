from Excptions.LibraryException import LibraryException


class AuthenticationException(LibraryException):
    """Base exception for authentication errors."""
    pass

class InvalidCredentialsException(AuthenticationException):
    """Raised when the provided credentials are invalid."""
    def __init__(self):
        super().__init__("Invalid username or password.")
