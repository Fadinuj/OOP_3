from tkinter import messagebox


class LibrarianObserver:
    """
    Observer class for notifying the librarian about updates in the system.

    This class provides a mechanism to display real-time notifications to the librarian
    using message boxes. It supports different types of messages such as information,
    warnings, and errors.
    """

    @staticmethod
    def notify(type, title, message):
        """
        Notify the current librarian with a message.

        Since the app is designed to work with one librarian at a time (no server),
        this method uses message boxes to display notifications directly.

        :param type: The type of notification ("message", "warning", "error").
        :param title: The title of the notification box.
        :param message: The content of the message to display.
        """
        if type == "message":
            messagebox.showinfo(f"{title}", f"Librarian: \n{message}")
        elif type == "warning":
            messagebox.showwarning(f"{title}", f"Librarian: \n{message}")
        elif type == "error":
            messagebox.showerror(f"{title}", f"Librarian: \n{message}")
        else:
            raise ValueError(f"Unknown notification type: {type}")
