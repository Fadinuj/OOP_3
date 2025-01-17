from Excptions.FieldException import FieldException


class InvalidNumericFieldException(FieldException):
    """
    Raised when a numeric field contains invalid data.
    """
    def __init__(self, field_name, invalid_value):
        super().__init__(f"The field '{field_name}' must be a valid number. Provided: {invalid_value}.")
