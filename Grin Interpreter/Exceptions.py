class GrinException(Exception):
    """
    Custom exception class for Grin interpreter errors.

    Attributes:
    - errorMessage (str): Error message describing the encountered exception.

    Methods:
    - __init__(errorMessage: str): Initializes the GrinException with an error message.
    """
    def __init__(self, errorMessage: str):
        """
        Initializes the GrinException with the provided error message.

        Args:
        - errorMessage (str): Error message describing the encountered exception.
        """
        self.errorMessage = errorMessage

