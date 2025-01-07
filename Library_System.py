import tkinter as tk
from tkinter import messagebox
from Book_window import Book_window
from Book import Book  # Assuming the Book class handles book operations
from All_books import All_books

class Library_System:
    def __init__(self, previous_window, background_image):
        previous_window.withdraw()
        library_system = tk.Toplevel(previous_window)
        library_system.geometry("800x600")
        library_system.title("Library System")
        library_system.state('zoomed')

        background_label_library = tk.Label(library_system, image=background_image)
        background_label_library.place(relwidth=1, relheight=1)

        frame = tk.Frame(library_system, bg="#8B644A", bd=5)
        frame.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(frame, text="Welcome to the Library System", font=("Arial", 18), bg="#8B644A", fg="white") \
            .grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        # Add buttons for different library operations
        tk.Button(frame, text="Add Book", font=("Arial", 14), width=15,
                  command=lambda: self.new_book(library_system, background_image)) \
            .grid(row=1, column=1, padx=10, pady=5)

        tk.Button(frame, text="View Books", font=("Arial", 14), width=15,
                  command=lambda: self.view_books(library_system, background_image)) \
            .grid(row=3, column=1, padx=10, pady=5)

        tk.Button(frame, text="Back", font=("Arial", 14), width=15,
                  command=lambda: self.back_to_main_page(library_system, previous_window)) \
            .grid(row=4, column=1, padx=10, pady=5)



    def remove_book(self, remove_entry):
        title = remove_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Please enter a book title.")
            return

        if Book.remove_book(title):  # Assuming Book.remove_book(title) returns True if successful
            messagebox.showinfo("Success", f"Book '{title}' has been removed.")
            remove_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Book '{title}' not found.")

    def view_books(self, previous_window, background_image):
        All_books(previous_window, background_image)

    def back_to_main_page(self, current_window, previous_window):
        current_window.destroy()  # Close the current window
        previous_window.deiconify()  # Show the main window again

    def new_book(self , library_system, background_image):
        Book_window(library_system, background_image)