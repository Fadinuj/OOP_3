import tkinter as tk
from tkinter import PhotoImage, messagebox
from User import User
from Library_System import Library_System


class Login:
    def __init__(self, previous_window, background_image):
        previous_window.withdraw()  # Hide the previous window
        login_window = tk.Toplevel(previous_window)
        login_window.geometry("1000x800")
        login_window.title("Login")
        login_window.state('zoomed')

        background_label_login = tk.Label(login_window, image=background_image)
        background_label_login.place(relwidth=1, relheight=1)

        frame = tk.Frame(login_window, bg="#8B644A", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="UserName:", font=("Arial", 14), bg="#8B644A").grid(row=0, column=0, padx=10, pady=5)
        username_entry = tk.Entry(frame, font=("Arial", 14))
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 14), bg="#8B644A").grid(row=1, column=0, padx=10, pady=5)
        password_entry = tk.Entry(frame, font=("Arial", 14), show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(frame, text="Enter", font=("Arial", 14), width=10,
                  command=lambda: submit_login(username_entry, password_entry, login_window, background_image)) \
            .grid(row=2, columnspan=2, pady=10)

        tk.Button(frame, text="Back", font=("Arial", 14), width=10,
                  command=lambda: back_to_main_page(login_window, previous_window)) \
            .grid(row=3, columnspan=2, pady=10)


def back_to_main_page(current_window , previous_window):
    current_window.destroy()  # Close the current window
    previous_window.deiconify()  # Show the main window again

def submit_login(username_entry, password_entry, previous_window , background_image):
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if User.authenticate(username, password):
        Library_System(previous_window,background_image)
    else:
        messagebox.showerror("Error", "Invalid username or password.")
