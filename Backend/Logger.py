import logging

class Logger:
    @staticmethod
    def log_info(message):
        """Log an informational message."""
        logging.info(message)

    @staticmethod
    def log_warning(message):
        """Log a warning message."""
        logging.warning(message)

    @staticmethod
    def log_error(message):
        """Log an error message."""
        logging.error(message)
