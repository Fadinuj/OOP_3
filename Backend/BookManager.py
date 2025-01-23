import csv

from Backend.LibrarianObserver import LibrarianObserver
from Backend.Logger import Logger
from Excptions.EmptyFieldException import EmptyFieldException

from Backend.Book import Book


class BookManager:
    books = []  # List to store books as dictionaries
    def load_books(self,book_file):
         """Load books from the CSV file into the list."""
    try:
        with open(Book.book_file, mode='r') as file:
            reader = csv.DictReader(file)
            books.clear()  # נקה את הרשימה לפני הטעינה
            for row in reader:
                # יצירת אובייקט ספר עם גישה לפי שמות העמודות
                book = Book(
                    title=row['Title'],
                    author=row['Author'],
                    is_loanen=row['Is Loanen'],
                    copies=int(row['Copies']),
                    available_copies=int(row['Available Copies']),
                    genre=row['Genre'],
                    year=int(row['Year'])
                )
                books.append(book)
    except FileNotFoundError:
        print("Books file not found. Starting with an empty list.")

    @classmethod
    def save_books_to_csv(cls):
        """Save the current list of books to the CSV file."""
        with open('books.csv', mode='w', newline='') as file:
            fieldnames = ['Title', 'Author', 'Is Loanen', 'Copies', 'Available Copies', 'Genre', 'Year']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for book in cls.books:
                writer.writerow({
                    'Title': book.title,
                    'Author': book.author,
                    'Is Loanen': book.is_loanen,
                    'Copies': book.copies,
                    'Available Copies': book.available_copies,
                    'Genre': book.genre,
                    'Year': book.year
                })
    def save_books(self):
        """Save the current list of books back to the CSV file."""
        with open(self.book_file, mode='w', newline='') as file:
            fieldnames = ["Title", "Author", "Is Loanen", "Copies", "Available Copies", "Genre", "Year"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.books)

    def add_book(self, title_entry, author_entry, is_loanen_var, copies_entry, genre_entry, year_entry):
        """Function to handle adding a new book."""
        title = title_entry.get().strip()
        author = author_entry.get().strip()
        is_loanen = is_loanen_var
        copies = copies_entry.get().strip()
        genre = genre_entry.get().strip()
        year = year_entry.get().strip()
        if not title:
            raise EmptyFieldException("Title")
        if not author:
            raise EmptyFieldException("Author")
        if not copies:
            raise EmptyFieldException("Copies")
        if not genre:
            raise EmptyFieldException("Genre")
        if not year:
            raise EmptyFieldException("Year")

        try:
            copies = int(copies) or 1
            year = int(year)

            # Check if the book already exists in the list of objects
            existing_book = next((book for book in BookManager.books if
                                  str(book.title) == str(title) and
                                  str(book.author) == str(author) and
                                  str(book.genre) == str(genre) and
                                  int(book.year) == int(year)), None)

            if existing_book:
                # Update the number of copies if the book exists
                existing_book.copies += copies
                existing_book.available_copies += copies
                Logger.log_warning(
                    f"Failed to add book: '{title}' by '{author}' already exists, and the copies were updated.")
                LibrarianObserver.notify(self, "message", "Info", f"Updated copies for '{title}'.")
            else:
                # Create a new object and add it to the list of books
                new_book = Book(title, author, is_loanen, copies, copies, genre, year)
                BookManager.books.append(new_book)
                Logger.log_info(f"Book '{title}' by '{author}' added successfully.")
                LibrarianObserver.notify(self, "Message", "Success",
                                         f"Book '{title}' by '{author}' added successfully.")

            # Save to the file after updating the list
            BookManager.save_books_to_csv()

        except ValueError:
            LibrarianObserver.notify(self, "Error", "Error", "Copies and Year must be valid numbers.")

    def update_copies(self, title, author, year, delta):
        """Update the number of available copies for a book."""
        for book in self.books:
            if book['Title'].lower() == title.lower() and book['Author'].lower() == author.lower() and int(book['Year']) == int(year):
                if 0 <= book['Available Copies'] + delta <= book['Copies']:
                    book['Available Copies'] += delta
                    book['Is Loanen'] = "Yes" if book['Available Copies'] < book['Copies'] else "No"
                    self.save_books()
                    return f"Copies of '{title}' have been updated."
                else:
                    return "Invalid update: copies cannot exceed total copies or be negative."
        return "Book not found."


    def sort_books(self, field):
        """
        Sort the books in the manager by a specified field.

        :param field: The field by which to sort the books (e.g., 'title', 'author', 'genre', 'year').
        :return: A sorted list of Book objects.
        """
        try:
            # Map the field to the corresponding attribute in the Book class
            field_mapping = {
                "Title": "title",
                "Author": "author",
                "Genre": "genre",
                "Year": "year",
            }

            # Check if the field is valid
            if field not in field_mapping:
                raise ValueError(f"Invalid field '{field}' for sorting.")

            # Sort the books based on the chosen field
            if field == "Title":
                sorted_books = sorted(BookManager.books, key=lambda book: book.get_title())
                Logger.log_info(f"Displayed books by {field} successfully")
            elif field == "Author":
                sorted_books = sorted(BookManager.books, key=lambda book: book.get_author())
                Logger.log_info(f"Displayed books by {field} successfully")
            elif field == "Genre":
                sorted_books = sorted(BookManager.books, key=lambda book: book.get_genre())
                Logger.log_info(f"Displayed books by {field} successfully")
            elif field == "Year":
                sorted_books = sorted(BookManager.books, key=lambda book: book.get_year())
                Logger.log_info(f"Displayed books by {field} successfully")
            return sorted_books

        except Exception as e:
            print(f"Error sorting books: {e}")
            return []

    def get_loaned_books(self, books):
        """
        Get all books that are currently loaned (is_loanen == 'Yes').

        :return: A list of Book objects that are loaned.
        """
        loaned_books = []
        try:
            for book in books:
                if book.available_copies < book.copies:  # Check the loaned status
                    loaned_books.append(book)
            return loaned_books
        except Exception as e:
            print(f"Error retrieving loaned books: {e}")
            return []

    def get_popular_books(self, threshold=3):
        """Return a list of popular books with more than a given number of copies."""
        return [book for book in self.books if book['Copies'] > threshold]
