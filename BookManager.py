import csv
from tkinter import ttk, messagebox

from Book import Book


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

        if not (title and author and copies and genre and year):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            copies = int(copies) or 1
            year = int(year)

            # בדיקה אם הספר כבר קיים ברשימת האובייקטים
            existing_book = next((book for book in BookManager.books if
                                  book.title == title and book.author == author and book.genre== genre.book.year == year), None)

            if existing_book:
                # עדכון מספר העותקים אם הספר קיים
                existing_book.copies += copies
                existing_book.available_copies += copies
                messagebox.showinfo("Info", f"Updated copies for '{title}'.")
            else:
                # יצירת אובייקט חדש והוספה לרשימת הספרים
                new_book = Book(title, author, is_loanen, copies, copies, genre, year)
                BookManager.books.append(new_book)
                messagebox.showinfo("Success", "Book added successfully!")

            # שמירה לקובץ לאחר עדכון הרשימה
            BookManager.save_books_to_csv()

        except ValueError:
            messagebox.showerror("Error", "Copies and Year must be valid numbers.")


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

    def search_books(self, keyword, books):
        """
        Search for books in the books list that match the given keyword.

        :param keyword: A string to search for in book attributes (case-insensitive).
        :return: A list of Book objects that match the keyword across all fields.
        """
        keyword = keyword.strip().lower()  # Strip whitespace and convert to lowercase

        # Filter books based on the keyword appearing in any attribute
        matching_books = [
            book for book in books
            if keyword in book.title.lower() or
               keyword in book.author.lower() or
               keyword in str(book.copies).lower() or
               keyword in str(book.available_copies).lower() or
               keyword in book.genre.lower() or
               keyword in str(book.year).lower()
        ]

        return matching_books

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
            elif field == "Author":
                sorted_books = sorted(BookManager.books, key=lambda book: book.get_author())
            elif field == "Genre":
                sorted_books = sorted(BookManager.books, key=lambda book: book.get_genre())
            elif field == "Year":
                sorted_books = sorted(BookManager.books, key=lambda book: book.get_year())
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
                if book.get_is_loanen() == "Yes":  # Check the loaned status
                    loaned_books.append(book)
            return loaned_books
        except Exception as e:
            print(f"Error retrieving loaned books: {e}")
            return []

    def get_popular_books(self, threshold=3):
        """Return a list of popular books with more than a given number of copies."""
        return [book for book in self.books if book['Copies'] > threshold]
