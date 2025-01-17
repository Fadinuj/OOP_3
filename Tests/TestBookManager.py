import unittest
from unittest.mock import patch, mock_open
from Backend.BookManager import BookManager

class TestBookManager(unittest.TestCase):
    def setUp(self):
        # Reset the books list before each test
        BookManager.books = []

    def test_add_book(self):
        BookManager.add_book("Sample Title", "Author Name", "Fiction", 2023)
        self.assertEqual(len(BookManager.books), 1)
        self.assertEqual(BookManager.books[0]["title"], "Sample Title")

    def test_load_books_from_csv(self):
        mock_csv_data = "Title,Author,Genre,Year\nSample Book,Author,Genre,2023\n"
        with patch("builtins.open", mock_open(read_data=mock_csv_data)):
            BookManager.load_books_from_csv("books.csv")
        self.assertEqual(len(BookManager.books), 1)
        self.assertEqual(BookManager.books[0]["title"], "Sample Book")

    def test_add_duplicate_book(self):
        BookManager.add_book("Sample Title", "Author Name", "Fiction", 2023)
        with self.assertRaises(Exception) as context:
            BookManager.add_book("Sample Title", "Author Name", "Fiction", 2023)
        self.assertEqual(str(context.exception), "Book already exists.")
