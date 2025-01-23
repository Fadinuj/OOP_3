import logging

class Logger:
    @staticmethod
    def setup_logger(log_file="app.log"):
        """
        Set up a logger to log messages to both a file and the console.

        :param log_file: Path to the log file.
        """
        # Create a logger instance
        logger = logging.getLogger("LibrarySystem")
        logger.setLevel(logging.DEBUG)  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        # Create handlers
        file_handler = logging.FileHandler(log_file)  # Log to file
        file_handler.setLevel(logging.DEBUG)  # File will log all levels

        console_handler = logging.StreamHandler()  # Log to console
        console_handler.setLevel(logging.INFO)  # Console will show only INFO and above

        # Create a formatter for better readability
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    @staticmethod
    def log_info(message):
        """Log an informational message."""
        logging.getLogger("LibrarySystem").info(message)

    @staticmethod
    def log_warning(message):
        """Log a warning message."""
        logging.getLogger("LibrarySystem").warning(message)

    @staticmethod
    def log_error(message):
        """Log an error message."""
        logging.getLogger("LibrarySystem").error(message)

    @staticmethod
    def log_critical(message):
        """Log a critical error message."""
        logging.getLogger("LibrarySystem").critical(message)
