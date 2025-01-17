class FieldException(Exception):
    """
    Base exception for field-related errors in the library system.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message
