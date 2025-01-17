from Excptions.UserException import UserException


class UserAlreadyExistsException(UserException):
    """Raised when trying to add a user that already exists."""
    def __init__(self, username):
        super().__init__(f"User '{username}' already exists.")
