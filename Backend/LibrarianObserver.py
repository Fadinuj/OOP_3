from tkinter import messagebox


class LibrarianObserver:
    """
    Observer class for notifying the librarian about updates in the system.
    """
    def notify(self, type, title ,message):
        """
        Notify the current librarian with a message.

        :param message: The message to display to the librarian.
        """
        if type == "message":
            messagebox.showinfo(f"{title}\n", f"Librarian: \n{message}")
        elif type == "warning":
            messagebox.showwarning(f"{title}\n", f"Librarian: \n{message}")
        elif type == "error":
            messagebox.showerror(f"{title}\n", f"Librarian: \n{message}")
