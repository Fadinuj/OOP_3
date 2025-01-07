import tkinter as tk
from tkinter import  messagebox
from User import User


class Register:
    def __init__(self, previous_window, background_image):
        previous_window.withdraw()  # Hide the previous window
        register_window = tk.Toplevel(previous_window)
        register_window.geometry("800x600")
        register_window.title("Register")
        register_window.state('zoomed')

        background_label_register = tk.Label(register_window, image=background_image)
        background_label_register.place(relwidth=1, relheight=1)

        frame = tk.Frame(register_window, bg="#8B644A", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="UserName:", font=("Arial", 14), bg="#8B644A").grid(row=0, column=0, padx=10, pady=5)
        username_entry = tk.Entry(frame, font=("Arial", 14))
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 14), bg="#8B644A").grid(row=1, column=0, padx=10, pady=5)
        password_entry = tk.Entry(frame, font=("Arial", 14), show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        def submit_register():
            username = username_entry.get()
            password = password_entry.get()

            if not username or not password:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            if User.user_exists(username):
                messagebox.showerror("Error", "Username already exists.")
            else:
                User(username, password)
                messagebox.showinfo("Success", "User registered successfully!")
                back_to_main_page(register_window,previous_window)
        tk.Button(frame, text="Register", font=("Arial", 14), width=10, command=submit_register).grid(row=2, columnspan=2, pady=10)
        tk.Button(frame, text="Back", font=("Arial", 14), width=10, command=lambda: back_to_main_page(register_window , previous_window)).grid(row=3, columnspan=2, pady=10)
def back_to_main_page(current_window , previous_window):
    current_window.destroy()  # Close the current window
    previous_window.deiconify()  # Show the main window again