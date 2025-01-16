import hashlib
import csv
from tkinter import messagebox


class User:
    users_file = 'users.csv'
    def __init__(self, username, password, active='NO'):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.active = active


    @staticmethod
    def hash_password(password):
        """Hash the password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def save_user(self):
        """Save user details to the users.csv file."""
        with open(User.users_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, self.password_hash , self.active])


    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user by checking the username and password."""
        password_hash = cls.hash_password(password)
        try:
            with open(cls.users_file, mode='r') as file:
                reader = csv.reader(file)
                flag = False
                for row in reader:
                    if flag:
                        if row[0] == username and row[1] == password_hash:
                            return True
                    flag = True
        except FileNotFoundError:
            messagebox.showerror("Error", "Users file not found.")
        return False

    @staticmethod
    def user_exists(username):
        """Check if a username already exists in the users.csv file."""
        try:
            with open(User.users_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == username:
                        return True
        except FileNotFoundError:
            return False
        return False
