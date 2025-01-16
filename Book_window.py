import tkinter as tk
from tkinter import messagebox, ttk
from Book import Book  # Assuming the Book class is in Book.py
from BookManager import BookManager

class Book_window:
    def __init__(self, previous_window, background_image):
        previous_window.withdraw()
        book_window = tk.Toplevel(previous_window)
        book_window.geometry("800x600")
        book_window.title("Add New Book")
        book_window.state('zoomed')

        background_label = tk.Label(book_window, image=background_image)
        background_label.place(relwidth=1, relheight=1)

        frame = tk.Frame(book_window, bg="#8B644A", bd=5)
        frame.place(relx=0.5, rely=0.4, anchor="center")

        # Labels and Entry fields for book details
        tk.Label(frame, text="Title:", font=("Arial", 14), bg="#8B644A", fg="white").grid(row=0, column=0, padx=10,
                                                                                          pady=5)
        title_entry = tk.Entry(frame, font=("Arial", 14))
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Author:", font=("Arial", 14), bg="#8B644A", fg="white").grid(row=1, column=0, padx=10,
                                                                                           pady=5)
        author_entry = tk.Entry(frame, font=("Arial", 14))
        author_entry.grid(row=1, column=1, padx=10, pady=5)



        tk.Label(frame, text="Copies:", font=("Arial", 14), bg="#8B644A", fg="white").grid(row=2, column=0, padx=10,
                                                                                           pady=5)
        copies_entry = tk.Entry(frame, font=("Arial", 14))
        copies_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame, text="Genre:", font=("Arial", 14), bg="#8B644A", fg="white").grid(row=3, column=0, padx=10,
                                                                                          pady=5)
        genre_entry = tk.Entry(frame, font=("Arial", 14))
        genre_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame, text="Year:", font=("Arial", 14), bg="#8B644A", fg="white").grid(row=4, column=0, padx=10,
                                                                                         pady=5)
        year_entry = tk.Entry(frame, font=("Arial", 14))
        year_entry.grid(row=4, column=1, padx=10, pady=5)

        # Button to submit the book details
        tk.Button(frame, text="Add Book", font=("Arial", 14), width=10,
                  command=lambda: self.add_book(title_entry, author_entry,'No', copies_entry, genre_entry,
                                                year_entry)) \
            .grid(row=6, columnspan=2, pady=10)

        # Button to go back to the previous window
        tk.Button(frame, text="Back", font=("Arial", 14), width=10,
                  command=lambda: self.back_to_previous(book_window, previous_window)) \
            .grid(row=7, columnspan=2, pady=10)

    def add_book(self, title_entry, author_entry, is_loanen_var, copies_entry, genre_entry, year_entry):
        BookManager.add_book(self, title_entry, author_entry, is_loanen_var, copies_entry, genre_entry, year_entry)

    def back_to_previous(self, current_window, previous_window):
        """Function to go back to the previous window."""
        current_window.destroy()
        previous_window.deiconify()

