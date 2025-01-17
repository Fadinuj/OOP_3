import csv
from Backend.Logger import Logger
class WaitlistManager:
    waitlist_file = 'Waitlist.csv'
    waitlist = []  # רשימת המתנה (רשימת מילונים)
    def load_waitlist_from_csv(self):
        """טוען את רשימת ההמתנה מקובץ ה-CSV."""
    try:
        with open(waitlist_file, mode='r') as file:
            waitlist.clear()
            reader = csv.DictReader(file)
            for row in reader:
                waitlist.append({
                    "Book Title": row["Book Title"],
                    "Author": row["Author"],
                    "Year": row["Year"],
                    "Name": row["Name"],
                    "Phone": row["Phone"],
                    "Email": row["Email"]
                })

    except FileNotFoundError:
        print("Waitlist file not found. Starting with an empty list.")

    def save_waitlist_to_csv(self):
        """
        Saves the current waitlist to the CSV file.

        This function writes the current state of the waitlist, stored as a list of dictionaries,
        to the specified CSV file. Each dictionary entry must contain the fields:
        "Book Title", "Name", "Phone", "Email".
        """
        try:
            with open(self.waitlist_file, mode='w', newline='') as file:
                fieldnames = ["Book Title", "Author","Year","Name", "Phone", "Email"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                # Validate and write each entry
                for entry in self.waitlist:
                    if all(key in entry for key in fieldnames):  # Ensure all required keys are present
                        writer.writerow(entry)
                    else:
                        print(f"Skipping invalid entry: {entry}")

        except Exception as e:
            print(f"Error saving waitlist to CSV: {e}")

    def remove_from_waitlist(self, book_title, author_name, year, waitlist):
        """
        Removes the first customer from the waitlist for a specific book.

        :param book_title: The title of the book.
        :param author_name: The author of the book.
        :param year: The publication year of the book.
        :param waitlist: The current waitlist as a list of dictionaries.
        :return: The removed customer entry, or None if no customer was found.
        """
        # Column headers to be preserved
        header = ["Book Title", "Author", "Year", "Name", "Phone", "Email"]

        for entry in waitlist:
            if (
                    entry["Book Title"] == book_title and
                    entry["Author"] == author_name and
                    int(entry["Year"]) == int(year)
            ):
                waitlist.remove(entry)
                Logger.log_info(f"User '{entry['Name']}' removed from waitlist for book: {book_title}.")
                # Save the updated waitlist
                with open(self.waitlist_file, 'w', newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=header)
                    writer.writeheader()  # Write the header first
                    writer.writerows(waitlist)  # Write the remaining waitlist entries
                return entry  # Return the removed customer
        return None  # Return None if no matching customer is found

