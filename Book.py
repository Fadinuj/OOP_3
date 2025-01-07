import csv
from tkinter import messagebox


class Book:
    book_file = 'books.csv'

    def __init__(self, title, author, is_loanen, copies, genre, year):
        self.title = title
        self.author = author
        self.is_loanen = is_loanen
        self.copies = copies
        self.genre = genre
        self.year = year
        self.save_book()

    @staticmethod
    def check_if_exists(title):
        """Check if a book with the given title already exists."""
        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0].strip().lower() == title.strip().lower():
                        return True
        except FileNotFoundError:
            pass
        return False

    @staticmethod
    def update_copies(title, additional_copies):
        """Update the number of copies for an existing book."""
        updated_rows = []
        book_found = False
        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0].strip().lower() == title.strip().lower():
                        row[3] = str(int(row[3]) + additional_copies)
                        book_found = True
                    updated_rows.append(row)
        except FileNotFoundError:
            messagebox.showerror("Error", "Books file not found.")
            return

        if book_found:
            with open(Book.book_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            messagebox.showinfo("Success", f"Copies of '{title}' updated successfully!")
        else:
            messagebox.showerror("Error", f"Book '{title}' not found.")

    def save_book(self):
        with open(Book.book_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.title, self.author, self.is_loanen, self.copies, self.genre, self.year])

    @classmethod
    def get_all_books(cls):
        """Retrieve all books from the books.csv file."""
        books = []
        try:
            with open(cls.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    books.append(row)
        except FileNotFoundError:
            print("Books file not found.")
        return books

    @classmethod
    def search_books(cls, keyword):
        """Search for books by a keyword in title or author."""
        result = []
        for book in cls.get_all_books():
            if keyword.lower() in book[0].lower() or keyword.lower() in book[1].lower():
                result.append(book)
        return result

    @classmethod
    def remove_book(cls, title):
        """Remove a book by title from the books.csv file."""
        books = cls.get_all_books()
        books = [book for book in books if book[0].lower() != title.lower()]
        with open(cls.book_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(books)
        print(f"Book '{title}' has been removed.")

    @classmethod
    def update_book(cls, title, new_author=None, new_is_loanen=None, new_copies=None, new_genre=None, new_year=None):
        """Update details of a specific book by title."""
        books = cls.get_all_books()
        updated = False
        for book in books:
            if book[0].lower() == title.lower():
                if new_author:
                    book[1] = new_author
                if new_is_loanen is not None:
                    book[2] = new_is_loanen
                if new_copies:
                    book[3] = new_copies
                if new_genre:
                    book[4] = new_genre
                if new_year:
                    book[5] = new_year
                updated = True
        if updated:
            with open(cls.book_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(books)
            print(f"Book '{title}' has been updated.")
        else:
            print(f"Book '{title}' not found.")
