import unittest
from unittest.mock import patch
from Backend.Logger import Logger

class TestLogger(unittest.TestCase):
    @patch("logging.info")
    def test_log_info(self, mock_log):
        Logger.log_info("Test info message.")
        mock_log.assert_called_once_with("Test info message.")

    @patch("logging.warning")
    def test_log_warning(self, mock_log):
        Logger.log_warning("Test warning message.")
        mock_log.assert_called_once_with("Test warning message.")

    @patch("logging.error")
    def test_log_error(self, mock_log):
        Logger.log_error("Test error message.")
        mock_log.assert_called_once_with("Test error message.")
