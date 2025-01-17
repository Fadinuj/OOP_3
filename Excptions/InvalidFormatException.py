from Excptions.FieldException import FieldException


class InvalidFormatException(FieldException):
    """
    Raised when a field contains data in an invalid format.
    """
    def __init__(self, field_name, expected_format):
        super().__init__(f"The field '{field_name}' must match the format: {expected_format}.")
