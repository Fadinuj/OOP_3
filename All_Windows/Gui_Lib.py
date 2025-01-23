import tkinter as tk
from All_Windows.Register import Register
from All_Windows.Login_window import Login
from Backend.Logger import Logger

root = tk.Tk()
root.geometry("800x600")
root.title("Main Page")
root.state('zoomed') # Open in full screen
Logger.setup_logger()
# Frame to center buttons
frame = tk.Frame(root, bg="#ffffff", bd=5)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Add buttons for Login, Register, and Exit
tk.Button(frame, text="Login", font=("Arial", 14), width=15, command=lambda: login_clicked(root))\
    .grid(row=0, column=0, padx=10, pady=10)

tk.Button(frame, text="Register", font=("Arial", 14), width=15, command=lambda: register_clicked(root))\
    .grid(row=1, column=0, padx=10, pady=10)

tk.Button(frame, text="Exit", font=("Arial", 14), width=15, command=root.quit)\
    .grid(row=2, column=0, padx=10, pady=10)

def login_clicked(previous_window):
    Login(previous_window)
def register_clicked(previous_window):
    Register(previous_window)
root.mainloop()
