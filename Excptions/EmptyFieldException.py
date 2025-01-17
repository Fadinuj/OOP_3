from Excptions.FieldException import FieldException


class EmptyFieldException(FieldException):
    """
    Raised when a required field is empty.
    """
    def __init__(self, field_name):
        super().__init__(f"The field '{field_name}' cannot be empty.")
