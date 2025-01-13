import tkinter as tk
from tkinter import ttk, messagebox
import csv
from Book import Book  # Assuming Book class handles CSV file operations

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
                  command=lambda: self.sort_books(tree, "Title")).pack(side="left", padx=5)
        tk.Button(sort_frame, text="Sort by Author", font=("Arial", 12), width=12,
                  command=lambda: self.sort_books(tree, "Author")).pack(side="left", padx=5)
        tk.Button(sort_frame, text="Sort by Genre", font=("Arial", 12), width=12,
                  command=lambda: self.sort_books(tree, "Genre")).pack(side="left", padx=5)
        tk.Button(sort_frame, text="Sort by Year", font=("Arial", 12), width=12,
                  command=lambda: self.sort_books(tree, "Year")).pack(side="left", padx=5)

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

    def load_books(self):
        """Load books from the CSV file into the Treeview."""
        # Clear existing rows in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    title, author, is_loanen, copies, available_copies, genre, year = row
                    self.tree.insert("", "end", values=(title, author, is_loanen, copies, available_copies, genre, year))
        except FileNotFoundError:
            messagebox.showinfo("Info", "No books found.")

    def search_books(self):
        """Search and filter books based on the search entry."""
        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.load_books()
            return

        # Clear existing rows in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Load and filter rows based on the search keyword
        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if any(keyword in str(cell).lower() for cell in row):
                        self.tree.insert("", "end", values=row)
        except FileNotFoundError:
            messagebox.showinfo("Info", "No books found.")

    def lend_book(self):
        """Lend a selected book."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to lend.")
            return

        # Get the selected book's values
        book_values = self.tree.item(selected_item, "values")
        title, author, is_loanen, copies, available_copies, genre, year = book_values[0], book_values[1], book_values[
            2], int(book_values[3]), int(book_values[4]), book_values[5], int(book_values[6])

        if available_copies > 0:
            Book.update_available_copies(title, author, year, -1)  # Update available copies in the CSV
            if available_copies - 1 < copies:  # If no copies are available after lending, set is_loanen to "Yes"
                Book.update_book(title, new_is_loanen="Yes")
            messagebox.showinfo("Success", f"Book '{title}' has been lent.")
        else:
            # Open the waitlist window if no copies are available
            self.open_waitlist_window(title)

        # Reload the updated book list to reflect changes
        self.load_books()

    def return_book(self):
        """Return a selected book."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to return.")
            return

        # Get the selected book's values
        book_values = self.tree.item(selected_item, "values")
        title, author, genre, year = book_values[0], book_values[1], book_values[5], int(book_values[6])
        copies, available_copies = int(book_values[3]), int(book_values[4])
        is_loanen = book_values[2]

        if available_copies < copies:
            available_copies += 1
            if available_copies == copies:
                is_loanen = "No"
            Book.update_copies_and_status(title, author, year, available_copies, is_loanen)
            self.check_and_assign_waitlist(title, author, year)
            messagebox.showinfo("Success", f"Book '{title}' has been returned.")
        else:
            messagebox.showwarning("Warning", f"All copies of '{title}' are already in the library.")

        self.load_books()

    def open_waitlist_window(self, book_title):
        """Open a window to add a customer to the waitlist."""
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
                  command=lambda: self.add_to_waitlist(waitlist_window, book_title, name_entry.get(), phone_entry.get(),
                                                       email_entry.get())) \
            .pack(pady=20)

    def add_to_waitlist(self, window, book_title, name, phone, email):
        """Add a customer to the waitlist and save to the CSV file."""
        if not (name and phone and email):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        waitlist_entry = {"Book Title": book_title, "Name": name, "Phone": phone, "Email": email}
        waitlist = self.load_waitlist()
        waitlist.append(waitlist_entry)

        with open(self.waitlist_file, mode='w', newline='') as file:
            fieldnames = ["Book Title", "Name", "Phone", "Email"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(waitlist)

        messagebox.showinfo("Success", f"{name} has been added to the waitlist for '{book_title}'.")
        window.destroy()

    def check_and_assign_waitlist(self, book_title, author, year):
        """Check if there are customers in the waitlist for the returned book and assign it."""
        waitlist = self.load_waitlist()
        for entry in waitlist:
            if entry["Book Title"] == book_title:
                messagebox.showinfo("Info", f"Book '{book_title}' has been assigned to {entry['Name']}.")
                waitlist.remove(entry)
                Book.update_available_copies(book_title, author, year, -1)
                break

        with open(self.waitlist_file, mode='w', newline='') as file:
            fieldnames = ["Book Title", "Name", "Phone", "Email"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(waitlist)

        self.load_books()

    def load_waitlist(self):
        """Load the waitlist from the CSV file."""
        waitlist = []
        try:
            with open(self.waitlist_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    waitlist.append(row)
        except FileNotFoundError:
            pass
        return waitlist

    def sort_books(self, tree, column):
        """Sort books based on a specific column."""
        books = [(tree.item(item)["values"], item) for item in tree.get_children()]
        index_map = {"Title": 0, "Author": 1, "Is Loanen": 2, "Copies": 3, "Available Copies": 4, "Genre": 5, "Year": 6}

        column_index = index_map[column]

        try:
            books.sort(key=lambda x: int(x[0][column_index]))
        except ValueError:
            books.sort(key=lambda x: str(x[0][column_index]).lower())

        for index, (values, item) in enumerate(books):
            tree.move(item, "", index)

    @staticmethod
    def back_to_previous(current_window, previous_window):
        """Go back to the previous window."""
        current_window.destroy()
        previous_window.deiconify()

    def filter_loaned_books(self, tree):
        """Filter and display only loaned books."""
        for row in tree.get_children():
            tree.delete(row)

        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[2] == "Yes":
                        tree.insert("", "end", values=row)
        except FileNotFoundError:
            messagebox.showinfo("Info", "No books found.")

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
