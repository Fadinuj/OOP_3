import tkinter as tk
from tkinter import ttk, messagebox
import csv
from Book import Book  # Assuming Book class handles CSV file operations
from BookManager import BookManager
from WaitlistManager import WaitlistManager
from Strategy_Search import SearchContext, SearchByTitle, SearchByAuthor, SearchByGenre, SearchByYear


class All_books:
    waitlist_file = 'Waitlist.csv'  # Path to the waitlist CSV file

    def __init__(self, previous_window, background_image):
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
        search_frame = tk.Frame(login_window, bg="black")
        search_frame.place(relx=0.5, rely=0.25, anchor="center")
        tk.Label(search_frame, text="Search:", font=("Arial", 14), bg="black", fg="white").pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 14), width=30)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", font=("Arial", 12), command=lambda: self.search_books(tree)) \
            .pack(side="left", padx=5)

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
            messagebox.showinfo("Info", "No books found.")

    def search_books(self,tree):
        """
        Search and filter books based on a keyword entered in the search entry field.

        This function interacts with the BookManager to retrieve books matching the keyword.
        If the search entry field is empty, it reloads all books. Otherwise, it clears the TreeView
        and displays books matching the keyword based on any attribute (title, author, genre, etc.).
        """
        keyword = self.search_entry.get().strip().lower()

        # If the search entry is empty, reload all books
        if not keyword:
            self.load_books()
            return

        # Clear existing rows in the TreeView
        for row in self.tree.get_children():
            tree.delete(row)

        # Retrieve books matching the keyword using BookManager
        matching_books = BookManager.search_books(self,keyword,BookManager.books)

        # Populate the TreeView with the filtered books
        for book in matching_books:
            self.tree.insert("", "end", values=(book.title, book.author, book.is_loanen,
                                                book.copies, book.available_copies, book.genre, book.year))

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
            messagebox.showerror("Error", "Please select a book to lend.")
            return

        book_values = self.tree.item(selected_item, "values")
        title, author, year = book_values[0], book_values[1], int(book_values[6])

        # Search for the book in the list
        for book in BookManager.books:
            if book.title == title and book.author == author and book.year == year:
                if book.available_copies > 0:
                    book.available_copies -= 1
                    if book.available_copies < book.copies:
                        book.is_loanen = "Yes"  # Update loan status
                    messagebox.showinfo("Success", f"Book '{title}' has been lent.")
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
            messagebox.showerror("Error", "Please select a book to delete.")
            return

        # Extract the book details from the selected row
        book_values = self.tree.item(selected_item, "values")
        title, author, year = book_values[0], book_values[1], int(book_values[6])
        is_loanen = book_values[2]

        # Check if the book is currently loaned
        if is_loanen == "Yes":
            messagebox.showwarning("Warning", f"Cannot delete the book '{title}' because it is currently loaned.")
            return

        # Find and remove the book from the BookManager's list of books
        book_found = False
        for book in BookManager.books:
            if book.title == title and book.author == author and book.year == year:
                BookManager.books.remove(book)
                book_found = True
                break

        if not book_found:
            messagebox.showwarning("Warning", f"Book '{title}' not found in the system.")
            return

        # Save the updated book list to the CSV file
        BookManager.save_books_to_csv()

        # Refresh the Treeview to reflect the updated list
        self.load_books()

        # Show success message
        messagebox.showinfo("Success", f"Book '{title}' has been deleted.")

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
            messagebox.showerror("Error", "Please select a book to return.")
            return

        # Get the selected book's values from the Treeview
        book_values = self.tree.item(selected_item, "values")
        title, author, year = book_values[0], book_values[1], int(book_values[6])

        # Find the book in the BookManager's list
        for book in BookManager.books:
            if book.title == title and book.author == author and book.year == year:
                if book.available_copies < book.copies:  # Ensure that there are loaned copies to return
                    book.available_copies += 1

                    if book.available_copies == book.copies:
                        book.is_loanen = "No"  # Update the loan status if all copies are available

                    # Check and assign to the next customer on the waitlist
                    waitlist_entry = WaitlistManager.remove_from_waitlist(self,title, author, year,WaitlistManager.waitlist)
                    if waitlist_entry:
                        # Assign the book to the next customer in the queue
                        book.available_copies -= 1
                        book.is_loanen = "Yes"
                        messagebox.showinfo(
                            "Waitlist Update",
                            f"Book '{title}' has been assigned to {waitlist_entry['Name']} from the waitlist."
                        )

                    # Save the updated book list and waitlist to CSV files
                    BookManager.save_books_to_csv()

                    # Reload the books in the Treeview
                    self.load_books()
                    messagebox.showinfo("Success", f"Book '{title}' has been returned.")
                    return
                else:
                    messagebox.showwarning("Warning", f"All copies of '{title}' are already available.")
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
        if not (name and phone and email):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

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
            messagebox.showinfo("Success", f"{name} has been added to the waitlist for '{book_title}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update waitlist file: {e}")

        # Close the current window after the operation
        window.destroy()

    def check_and_assign_waitlist(self, book_title, author, year):
        """Check if there are customers in the waitlist for the returned book and assign it."""
        removed_entry = WaitlistManager.remove_from_waitlist(self, book_title,author,year,WaitlistManager.waitlist)
        if removed_entry:
            messagebox.showinfo("Info", f"Book '{book_title}' has been assigned to {removed_entry['Name']}.")
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
            print(f"Error sorting books: {e}")
            messagebox.showerror("Error", f"Failed to sort books by {field}.")

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

            # Insert filtered loaned books into the Treeview
            for book in loaned_books:
                tree.insert("", "end", values=(book.title, book.author, book.is_loanen,
                                               book.copies, book.available_copies,
                                               book.genre, book.year))
        except Exception as e:
            messagebox.showerror("Error", f"Could not filter loaned books: {e}")

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
        """Filter and display popular books (books with more than 3 copies)."""
        for row in tree.get_children():
            tree.delete(row)

        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if int(int(row[3]) - int(row[4])) > 3:
                        tree.insert("", "end", values=row)
        except FileNotFoundError:
            messagebox.showinfo("Info", "No books found.")
