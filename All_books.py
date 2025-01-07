import tkinter as tk
from tkinter import ttk, messagebox
import csv
from Book import Book  # Assuming Book class handles CSV file operations

class All_books:
    def __init__(self, previous_window, background_image):
        previous_window.withdraw()  # Hide the previous window
        login_window = tk.Toplevel(previous_window)
        login_window.geometry("800x600")
        login_window.title("All Books")
        login_window.state('zoomed')


        frame1 = tk.Frame(login_window, bg="black", bd=5)
        frame1.place(relx=0.5, rely=0.1, anchor="center")

        tk.Label(frame1, text="All Books", font=("Arial", 18), bg="black", fg="white").pack(pady=10)

        # Search bar
        search_frame = tk.Frame(login_window, bg="black")
        search_frame.place(relx=0.5, rely=0.2, anchor="center")
        tk.Label(search_frame, text="Search:", font=("Arial", 14), bg="black", fg="white").pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 14), width=30)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", font=("Arial", 12), command=lambda: self.search_books(tree)) \
            .pack(side="left", padx=5)

        # Create a Treeview widget to display all books
        columns = ("Title", "Author", "Is Loanen", "Copies", "Genre", "Year")
        tree = ttk.Treeview(login_window, columns=columns, show="headings")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Is Loanen", text="Is Loanen")
        tree.heading("Copies", text="Copies")
        tree.heading("Genre", text="Genre")
        tree.heading("Year", text="Year")

        tree.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.5)

        self.load_books(tree)

        tk.Button(frame1, text="Back", font=("Arial", 14), width=10,
                  command=lambda: self.back_to_previous(login_window, previous_window)) \
            .pack(pady=10)
        # Add Lend Book button
        tk.Button(login_window, text="Lend Book", font=("Arial", 12), width=15,
                  command=lambda: self.lend_selected_book(tree)) \
            .place(relx=0.35, rely=0.85, anchor="center")

        # Add Remove Book button
        tk.Button(login_window, text="Remove Book", font=("Arial", 12), width=15,
                  command=lambda: self.remove_selected_book(tree)) \
            .place(relx=0.65, rely=0.85, anchor="center")

    def load_books(self, tree):
        """Load books from the CSV file into the Treeview."""
        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    tree.insert("", "end", values=row)
        except FileNotFoundError:
            messagebox.showinfo("Info", "No books found.")

    def remove_selected_book(self, tree):
        """Remove the selected book from the Treeview and the CSV file."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to remove.")
            return

        # Get the values of the selected row
        book_values = tree.item(selected_item, "values")
        title = book_values[0]

        # Remove the selected row from the CSV file
        books = []
        with open(Book.book_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != title:  # Keep only books with a different title
                    books.append(row)

        with open(Book.book_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(books)

        # Remove the selected row from the Treeview
        tree.delete(selected_item)

    def search_books(self, tree):
        """Search and filter books based on the search entry."""
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a search keyword.")
            return

        # Clear existing rows in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Load and filter rows
        try:
            with open(Book.book_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if any(keyword in str(cell).lower() for cell in row):  # Check keyword in any cell
                        tree.insert("", "end", values=row)
        except FileNotFoundError:
            messagebox.showinfo("Info", "No books found.")

    def back_to_previous(self, current_window, previous_window):
        """Go back to the previous window."""
        current_window.destroy()
        previous_window.deiconify()

    def lend_selected_book(self, tree):
        """Mark the selected book as loaned and update the CSV file."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to lend.")
            return

        # Get the values of the selected row
        book_values = tree.item(selected_item, "values")
        title = book_values[0]

        # Update the selected row in the CSV file
        books = []
        updated = False
        with open(Book.book_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].strip().lower() == title.strip().lower() and row[2].lower() == "no":
                    row[2] = "Yes"  # Mark the book as loaned
                    updated = True
                books.append(row)

        if not updated:
            messagebox.showwarning("Warning", f"Book '{title}' is already loaned.")
            return

        # Write the updated rows back to the CSV file
        with open(Book.book_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(books)

        # Update the Treeview
        tree.item(selected_item, values=books[tree.index(selected_item)])

        messagebox.showinfo("Success", f"Book '{title}' has been loaned.")