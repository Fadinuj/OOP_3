import csv

from Book import Book


class BookManager:
    books = []  # List to store books as dictionaries
    book_file = 'books.csv'
    def load_books(self):
        """Load books from the CSV file into the list."""
        self.books.clear()
        try:
            with open(self.book_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = Book(self,row[0],row[1],row[2])
        except FileNotFoundError:
            print("Books file not found. Starting with an empty list.")

    def save_books(self):
        """Save the current list of books back to the CSV file."""
        with open(self.book_file, mode='w', newline='') as file:
            fieldnames = ["Title", "Author", "Is Loanen", "Copies", "Available Copies", "Genre", "Year"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.books)

    def add_book(self, title, author, genre, year, copies):
        """Add a new book or update copies if it already exists."""
        for book in self.books:
            if book['Title'].lower() == title.lower() and book['Author'].lower() == author.lower() and int(book['Year']) == int(year):
                book['Copies'] += copies
                book['Available Copies'] += copies
                self.save_books()
                return f"Copies of '{title}' have been updated."

        new_book = {
            "Title": title,
            "Author": author,
            "Is Loanen": "No",
            "Copies": copies,
            "Available Copies": copies,
            "Genre": genre,
            "Year": year
        }
        self.books.append(new_book)
        self.save_books()
        return f"Book '{title}' has been added."

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

    def search_books(self, keyword):
        """Search for books by a keyword in any field."""
        keyword = keyword.lower()
        return [book for book in self.books if any(keyword in str(value).lower() for value in book.values())]

    def sort_books(self, key):
        """Sort books based on a specific key."""
        try:
            self.books.sort(key=lambda x: (int(x[key]) if key in ['Copies', 'Available Copies', 'Year'] else x[key].lower()))
        except KeyError:
            print(f"Invalid key: '{key}'")

    def get_loaned_books(self):
        """Return a list of loaned books."""
        return [book for book in self.books if book['Is Loanen'] == "Yes"]

    def get_popular_books(self, threshold=3):
        """Return a list of popular books with more than a given number of copies."""
        return [book for book in self.books if book['Copies'] > threshold]
