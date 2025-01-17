import unittest
from unittest.mock import patch
from Backend.LibrarianObserver import LibrarianObserver

class TestLibrarianObserver(unittest.TestCase):
    @patch("tkinter.messagebox.showinfo")
    def test_notify_success(self, mock_messagebox):
        LibrarianObserver.notify("message", "Success", "Book added successfully.")
        mock_messagebox.assert_called_once_with("Success", "Book added successfully.")
