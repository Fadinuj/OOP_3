from BookDecorator import BookDecorator


class LoggingDecorator(BookDecorator):
    def display_details(self):
        """Log the book details before returning them."""
        details = self.book.display_details()
        self.log(details)
        return details

    @staticmethod
    def log(details):
        """Log the book details."""
        with open("book_logs.txt", "a") as log_file:
            log_file.write(details + "\n")
        print(f"Logged: {details}")
