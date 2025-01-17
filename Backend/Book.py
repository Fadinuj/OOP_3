import csv
from tkinter import messagebox

class Book:
    book_file = 'books.csv'
    def __init__(self, title, author, is_loanen, copies, available_copies, genre, year):
        self.title = title
        self.author = author
        self.is_loanen = is_loanen
        self.copies = int(copies)
        self.available_copies = int(available_copies)
        self.genre = genre
        self.year = int(year)

    def get_title(self):
        return self.title
    def get_author(self):
        return self.author
    def get_genre(self):
        return self.genre
    def get_year(self):
        return self.year
    def get_copies(self):
        return self.copies
    def get_available_copies(self):
        return self.available_copies
    def get_is_loanen(self):
        return self.is_loanen
    @staticmethod
    def update_copies_and_status(self, title, author, year, available_copies, is_loanen):
        """Update the number of available copies and the loan status for an existing book."""
        from BookManager import BookManager
        for book in BookManager.books:
            if book.title.strip().lower() == title.strip().lower() and \
                    book.author.strip().lower() == author.strip().lower() and \
                    int(book.year) == int(year):
                book.available_copies = available_copies
                book.is_loanen = is_loanen
                break
        BookManager.save_books_to_csv()  # שמירת השינויים לקובץ

    def save_books_to_csv(self):
        """Save the updated list of books to the CSV file."""
        from BookManager import BookManager
        with open(Book.book_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Author", "Is Loanen", "Copies", "Available Copies", "Genre", "Year"])
            for book in BookManager.books:
                writer.writerow(
                    [book.title, book.author, book.is_loanen, book.copies, book.available_copies, book.genre,
                     book.year])

    @staticmethod
    def check_if_exists(self, title, author, year):
        """Check if a book with the given title, author, and year already exists in the system."""
        for book in self.books:  # Assuming self.books is the list of Book objects
            if book.title.strip().lower() == title.strip().lower() and \
                    book.author.strip().lower() == author.strip().lower() and \
                    int(book.year) == int(year):
                return True
        return False

    @staticmethod
    def update_available_copies(title ,author, year, additional_copies):
        """Update the number of copies for an existing book."""
        updated_rows = []
        book_found = False
        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0].strip().lower() == title.strip().lower() and row[1].strip().lower()==author.strip().lower() and int (row[6])==int(year):
                        if int(row[4])+additional_copies <= int(row[3]):
                            row[4] = str(int(row[4]) + additional_copies)
                            book_found = True
                        else:
                            messagebox.showerror("Error", "All copies is in the library.!")
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


    @staticmethod
    def update_copies(title, author, year, additional_copies):
        """Update the number of copies for an existing book."""
        updated_rows = []
        book_found = False
        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0].strip().lower() == title.strip().lower() and row[
                        1].strip().lower() == author.strip().lower() and int(row[6]) == int(year):
                        row[4] = str(int(row[4]) + additional_copies)
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
            writer.writerow([self.title, self.author, self.is_loanen, self.copies,self.available_copies, self.genre, self.year])

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
