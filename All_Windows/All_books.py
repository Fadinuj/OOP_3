import tkinter as tk
from tkinter import ttk
import csv
from Backend.Book import Book  # Assuming Book class handles CSV file operations
from Backend.BookManager import BookManager
from Backend.WaitlistManager import WaitlistManager
from Backend.Strategy_Search import SearchContext, SearchByTitle, SearchByAuthor, SearchByGenre, SearchByYear
from Backend.Logger import Logger
from Backend.LibrarianObserver import LibrarianObserver
from Excptions.EmptyFieldException import EmptyFieldException

class All_books:
    waitlist_file = 'Waitlist.csv'  # Path to the waitlist CSV file

    def __init__(self, previous_window):
        previous_window.withdraw()  # Hide the previous window
        login_window = tk.Toplevel(previous_window)
        login_window.geometry("800x600")
        login_window.title("All Books")
        login_window.state('zoomed')

        frame1 = tk.Frame(login_window, bg="black", bd=5)
        frame1.place(relx=0.5, rely=0.1, anchor="center")

        tk.Label(frame1, text="All Books", font=("Arial", 18), bg="black", fg="white").pack(pady=10)

        # Sort buttons below the "All Books" label
        sort_frame = tk.Frame(login_window, bg="black")
        sort_frame.place(relx=0.5, rely=0.18, anchor="center")

        tk.Button(sort_frame, text="Sort by Title", font=("Arial", 12), width=12,
                  command=lambda: self.sort_books("Title")).pack(side="left", padx=5)
        tk.Button(sort_frame, text="Sort by Author", font=("Arial", 12), width=12,
                  command=lambda: self.sort_books("Author")).pack(side="left", padx=5)
        tk.Button(sort_frame, text="Sort by Genre", font=("Arial", 12), width=12,
                  command=lambda: self.sort_books("Genre")).pack(side="left", padx=5)
        tk.Button(sort_frame, text="Sort by Year", font=("Arial", 12), width=12,
                  command=lambda: self.sort_books("Year")).pack(side="left", padx=5)

        # New buttons for filtering loaned and popular books
        tk.Button(sort_frame, text="Loaned Books", font=("Arial", 12), width=12,
                  command=lambda: self.filter_loaned_books(tree)).pack(side="left", padx=5)
        tk.Button(sort_frame, text="Popular Books", font=("Arial", 12), width=12,
                  command=lambda: self.filter_popular_books(tree)).pack(side="left", padx=5)

        # Search bar
        # Search bar
        search_frame = tk.Frame(login_window, bg="black")
        search_frame.place(relx=0.5, rely=0.25, anchor="center")

        tk.Label(search_frame, text="Search:", font=("Arial", 14), bg="black", fg="white").pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 14), width=30)
        self.search_entry.pack(side="left", padx=5)

        # Search buttons
        tk.Button(search_frame, text="Search by Title", font=("Arial", 12), width=15,
                  command=lambda: self.search_books_by_strategy("Title")).pack(side="left", padx=5)
        tk.Button(search_frame, text="Search by Author", font=("Arial", 12), width=15,
                  command=lambda: self.search_books_by_strategy("Author")).pack(side="left", padx=5)
        tk.Button(search_frame, text="Search by Genre", font=("Arial", 12), width=15,
                  command=lambda: self.search_books_by_strategy("Genre")).pack(side="left", padx=5)
        tk.Button(search_frame, text="Search by Year", font=("Arial", 12), width=15,
                  command=lambda: self.search_books_by_strategy("Year")).pack(side="left", padx=5)

        # Create a Treeview widget to display all books with new column "Available Copies"
        columns = ("Title", "Author", "Is Loanen", "Copies", "Available Copies", "Genre", "Year")
        tree = ttk.Treeview(login_window, columns=columns, show="headings")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Is Loanen", text="Is Loanen")
        tree.heading("Copies", text="Copies")
        tree.heading("Available Copies", text="Available Copies")
        tree.heading("Genre", text="Genre")
        tree.heading("Year", text="Year")

        tree.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.8, relheight=0.5)

        self.tree = tree  # Store tree reference for reloading
        self.load_books()

        # Buttons for operations
        button_frame = tk.Frame(login_window, bg="black")
        button_frame.place(relx=0.5, rely=0.85, anchor="center")

        tk.Button(button_frame, text="Back", font=("Arial", 12), width=10,
                  command=lambda: self.back_to_previous(login_window, previous_window)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Lend Book", font=("Arial", 12), width=10,
                  command=self.lend_book).pack(side="left", padx=5)
        tk.Button(button_frame, text="Return Book", font=("Arial", 12), width=10,
                  command=self.return_book).pack(side="left", padx=5)
        tk.Button(button_frame, text="Remove Book", font=("Arial", 12), width=15,
                  command=self.delete_selected_book).pack(side="left", padx=5)

    def load_books(self):
        """Load books from the CSV file into the Treeview."""
        # Clear existing rows in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for index, row in enumerate(reader):
                    if index == 0:  # Skip the first row (header)
                        continue
                    title, author, is_loanen, copies, available_copies, genre, year = row
                    self.tree.insert("", "end",
                                     values=(title, author, is_loanen, copies, available_copies, genre, year))
        except FileNotFoundError:
            LibrarianObserver.notify(self,"message","Info", "No books found.")


    def lend_book(self):
        """
        Lends a book from the list of books.

        This function allows the user to lend a book by selecting it from the Treeview.
        If there are available copies of the selected book, it decreases the available copies count
        and updates the loan status to "Yes" if necessary. If no copies are available, a warning is displayed.

        Process:
        1. Checks if a book is selected in the Treeview.
        2. Searches the book in the BookManager's list of books.
        3. If available copies exist, decreases the available copies count.
           - Updates the loan status to "Yes" if any copies are loaned.
        4. If no available copies exist, shows a warning message.
        5. Saves the updated book list to the CSV file and refreshes the Treeview.

        :raises messagebox.showerror: If no book is selected.
        :raises messagebox.showwarning: If no available copies exist.
        :return: None
        """
        selected_item = self.tree.selection()
        if not selected_item:
            Logger.log_error("Error Please select a book to lend.")
            LibrarianObserver.notify(self,"error","Error", "Please select a book to lend.")
            return

        book_values = self.tree.item(selected_item, "values")
        title, author, year = book_values[0], book_values[1], int(book_values[6])

        # Search for the book in the list
        for book in BookManager.books:
            if book.title == title and book.author == author and book.year == year:
                if book.available_copies > 0:
                    book.available_copies -= 1
                    if book.available_copies == 0:
                        book.is_loanen = "Yes"  # Update loan status
                    Logger.log_info(f"Book '{title}' has been lent.")
                    LibrarianObserver.notify(self,"message","Success", f"Book '{title}' has been lent.")
                else:
                    # Open the waitlist window
                    self.open_waitlist_window(title, author, year)
                break

        # Save the updated book list to the CSV file and refresh the Treeview
        BookManager.save_books_to_csv()
        self.load_books()

    def delete_selected_book(self):
        """
        Deletes the selected book from the list and updates the CSV file.
        Prevents deletion of a book if it is currently loaned.
        """
        # Get the selected book from the Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            LibrarianObserver.notify(self,"error","Error", "Please select a book to delete.")
            return

        # Extract the book details from the selected row
        book_values = self.tree.item(selected_item, "values")
        title, author, year = book_values[0], book_values[1], int(book_values[6])
        copies , available_copies = book_values[3], book_values[4]
        is_loanen = book_values[2]

        # Check if the book is currently loaned
        if available_copies < copies:
            LibrarianObserver.notify(self,"warning","Warning", f"Cannot delete the book '{title}' because it is currently loaned.")
            return

        # Find and remove the book from the BookManager's list of books
        book_found = False
        for book in BookManager.books:
            if book.title == title and book.author == author and book.year == year:
                BookManager.books.remove(book)
                book_found = True
                break

        if not book_found:
            LibrarianObserver.notify(self,"warning","Warning",f"Book '{title}' not found in the system.")
            return

        # Save the updated book list to the CSV file
        BookManager.save_books_to_csv()

        # Refresh the Treeview to reflect the updated list
        self.load_books()

        # Show success message
        LibrarianObserver.notify(self,"message","Success", f"Book '{title}' has been deleted.")

    def search_books_by_strategy(self, field):
        """
        Search books using a specific strategy (e.g., by Title, Author, Genre, Year).
        :param field: The field to search by.
        """
        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.load_books()
            Logger.log_info("Displayed all books successfully/")
            return

        try:
            # Map strategies to search fields
            strategy_mapping = {
                "Title": SearchByTitle(),
                "Author": SearchByAuthor(),
                "Genre": SearchByGenre(),
                "Year": SearchByYear()
            }

            if field not in strategy_mapping:
                raise ValueError(f"Invalid search field: {field}")
                Logger.log_error("Error Please select a book to return.")

            # Use the selected search strategy
            search_context = SearchContext(strategy_mapping[field])
            matching_books = search_context.search(keyword, field,BookManager.books)

            # Clear existing rows in the Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Populate the TreeView with the filtered books
            for book in matching_books:
                self.tree.insert("", "end", values=(book.title, book.author, book.is_loanen,
                                                    book.copies, book.available_copies, book.genre, book.year))

        except Exception as e:
            LibrarianObserver.notify(self,"error","Error", f"Search failed with error: {e}")

    def return_book(self):
        """
        Returns a selected book.

        This function handles the process of returning a book:
        1. Checks if a book is selected in the Treeview.
        2. Updates the available copies count.
        3. Updates the loan status if all copies are available.
        4. Checks the waitlist for the book and assigns it to the next customer in the queue, if applicable.
        5. Saves the updated book list and waitlist to their respective CSV files.

        :raises messagebox.showerror: If no book is selected.
        :raises messagebox.showwarning: If all copies are already available.
        :return: None
        """
        selected_item = self.tree.selection()
        if not selected_item:
            LibrarianObserver.notify(self,"error","Error", "Please select a book to return.")
            Logger.log_error("Error Please select a book to return.")
            return

        # Get the selected book's values from the Treeview
        book_values = self.tree.item(selected_item, "values")
        title, author, year = book_values[0], book_values[1], int(book_values[6])

        # Find the book in the BookManager's list
        for book in BookManager.books:
            if book.title == title and book.author == author and book.year == year:
                if book.available_copies < book.copies:  # Ensure that there are loaned copies to return
                    book.available_copies += 1

                    if book.available_copies > 0:
                        book.is_loanen = "No"  # Update the loan status if all copies are available

                    # Check and assign to the next customer on the waitlist
                    waitlist_entry = WaitlistManager.remove_from_waitlist(self,title, author, year,WaitlistManager.waitlist)
                    if waitlist_entry:
                        # Assign the book to the next customer in the queue
                        book.available_copies -= 1
                        if(book.available_copies == 0):
                            is_loanen = "Yes"
                        LibrarianObserver.notify(self,"message","Waitlist Update",
                            f"Book '{title}' has been assigned to {waitlist_entry['Name']} from the waitlist.")
                        Logger.log_info(f"Book '{title}' has been assigned to {waitlist_entry['Name']} from the waitlist.")

                    # Save the updated book list and waitlist to CSV files
                    BookManager.save_books_to_csv()

                    # Reload the books in the Treeview
                    self.load_books()
                    LibrarianObserver.notify(self,"message","Success",f"Book '{title}' has been returned.")
                    Logger.log_info(f"Book '{title}' has been returned.")
                    return
                else:
                    LibrarianObserver.notify(self,"warning","Warning",f"Book '{title}' is already available.")
                    Logger.log_warning("Book '{title}' is already available.")
                    return

    def add_to_waitlist(self, window, book_title, author, year, name, phone, email):
        """
        Add a customer to the waitlist and update both the in-memory list and the CSV file.

        :param window: The current Tkinter window to close after adding the entry.
        :param book_title: The title of the book the customer is waiting for.
        :param author: The author of the book.
        :param genre: The genre of the book.
        :param year: The year of publication of the book.
        :param name: The name of the customer.
        :param phone: The phone number of the customer.
        :param email: The email address of the customer.
        """
        if not book_title.strip():
            raise EmptyFieldException("Book Title")
        if not name.strip():
            raise EmptyFieldException("Customer Name")
        if not phone.strip():
            raise EmptyFieldException("Phone")
        if not email.strip():
            raise EmptyFieldException("Email")

        # Create a new waitlist entry with additional attributes
        waitlist_entry = {
            "Book Title": book_title,
            "Author": author,
            "Year": year,
            "Name": name,
            "Phone": phone,
            "Email": email
        }

        # Add the entry to the in-memory waitlist (assume `self.waitlist` exists as a list)
        WaitlistManager.waitlist.append(waitlist_entry)

        # Save the updated waitlist to the CSV file
        try:
            with open(self.waitlist_file, mode='w', newline='') as file:
                fieldnames = ["Book Title", "Author","Year", "Name", "Phone", "Email"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(WaitlistManager.waitlist)
            Logger.log_info(f"User '{name}' added to waitlist for book: {book_title}.")
            LibrarianObserver.notify(self,"message","Success", f"{name} has been added to the waitlist for '{book_title}'.")

        except Exception as e:
            Logger.log_error(f"Error Failed to update waitlist file: {e}")
            LibrarianObserver.notify(self,"error","Error", f"Failed to update waitlist file: {e}")

        # Close the current window after the operation
        window.destroy()

    def check_and_assign_waitlist(self, book_title, author, year):
        """Check if there are customers in the waitlist for the returned book and assign it."""
        removed_entry = WaitlistManager.remove_from_waitlist(self, book_title,author,year,WaitlistManager.waitlist)
        if removed_entry:
            Logger.log_info(f"Book '{book_title}' has been assigned to {removed_entry['Name']}.")
            LibrarianObserver.notify(self,"message","Info", f"Book '{book_title}' has been assigned to {removed_entry['Name']}.")
            Book.update_available_copies(book_title, author, year, -1)


    def sort_books(self, field):
        """
        Sort the books displayed in the Treeview by the specified field.

        :param field: The field by which to sort the books (e.g., 'Title', 'Author', 'Copies', 'Year').
        """
        try:
            # Validate that the field exists in the Book object
            valid_fields = {"Title", "Author", "Copies", "Available Copies", "Genre", "Year"}
            if field not in valid_fields:
                raise ValueError(f"Invalid field '{field}' for sorting.")

            # Use BookManager to sort books
            sorted_books = BookManager.sort_books(self,field)

            # Clear the existing Treeview content
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Add the sorted books back to the Treeview
            for book in sorted_books:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                    book.title, book.author, book.is_loanen, book.copies, book.available_copies, book.genre, book.year),
                )

        except Exception as e:
            Logger.log_error(f"Error Failed to sort books: {field}")
            LibrarianObserver.notify(self,"error","Error", f"Failed to sort books by {field}.")

    @staticmethod
    def back_to_previous(current_window, previous_window):
        """Go back to the previous window."""
        current_window.destroy()
        previous_window.deiconify()

    def filter_loaned_books(self, tree):
        """Filter and display only loaned books."""
        # Clear existing rows in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        try:
            # Use the BookManager's function to filter loaned books
            loaned_books = BookManager.get_loaned_books(self,BookManager.books)  # Assuming book_manager is an instance of BookManager
            Logger.log_info(f"Displayed All loaned books successfully")
            # Insert filtered loaned books into the Treeview
            for book in loaned_books:
                tree.insert("", "end", values=(book.title, book.author, book.is_loanen,
                                               book.copies, book.available_copies,
                                               book.genre, book.year))
        except Exception as e:
            Logger.log_error(f"Error Failed to filter loaned books: {e}")
            LibrarianObserver.notify(self,"error","Error", f"Failed to filter loaned books: {e}")

    def open_waitlist_window(self, book_title, author, year):
        """
        Open a new window to add a customer to the waitlist for a specific book.

        :param book_title: The title of the book.
        :param author: The author of the book.
        :param year: The publication year of the book.
        """
        waitlist_window = tk.Toplevel()
        waitlist_window.geometry("400x300")
        waitlist_window.title(f"Add to Waitlist - {book_title}")
        waitlist_window.resizable(False, False)

        tk.Label(waitlist_window, text=f"Add to Waitlist for '{book_title}'", font=("Arial", 14)).pack(pady=10)

        # Entry fields for customer details
        tk.Label(waitlist_window, text="Name:", font=("Arial", 12)).pack(pady=5)
        name_entry = tk.Entry(waitlist_window, font=("Arial", 12))
        name_entry.pack(pady=5)

        tk.Label(waitlist_window, text="Phone:", font=("Arial", 12)).pack(pady=5)
        phone_entry = tk.Entry(waitlist_window, font=("Arial", 12))
        phone_entry.pack(pady=5)

        tk.Label(waitlist_window, text="Email:", font=("Arial", 12)).pack(pady=5)
        email_entry = tk.Entry(waitlist_window, font=("Arial", 12))
        email_entry.pack(pady=5)

        # Button to submit waitlist details
        tk.Button(waitlist_window, text="Add to Waitlist", font=("Arial", 12),
                  command=lambda: self.add_to_waitlist(waitlist_window, book_title, author, year,
                                                       name_entry.get(), phone_entry.get(), email_entry.get())) \
            .pack(pady=20)

    def filter_popular_books(self, tree):
        """
        Filter and display popular books in the Treeview (books with more than 3 total lent copies).

        A popular book is determined by the number of times it has been lent out (total copies - available copies).
        """
        # Clear existing rows in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        try:
            # Filter popular books based on the in-memory BookManager list
            popular_books = [
                book for book in BookManager.books
                if (int(book.copies) - int(book.available_copies)) > 3
            ]

            if not popular_books:
                Logger.log_info("No popular books found.")
                LibrarianObserver.notify(self, "message", "Info", "No popular books found.")
                return

            # Insert filtered books into the Treeview
            for book in popular_books:
                tree.insert(
                    "",
                    "end",
                    values=(
                        book.title, book.author, book.is_loanen, book.copies,
                        book.available_copies, book.genre, book.year
                    )
                )

            LibrarianObserver.notify(
                self, "message", "Info", f"Displayed {len(popular_books)} popular books."
            )
            Logger.log_info(f"Displayed {len(popular_books)} popular books.")
        except Exception as e:
            LibrarianObserver.notify(
                self, "error", "Error", f"Failed to filter popular books: {str(e)}"
            )
            Logger.log_error(f"Error Failed to filter popular books: {str(e)}")
