import hashlib
import csv
from tkinter import messagebox
from urllib.parse import uses_params

from Backend.User import User
from Excptions.AuthenticationException import AuthenticationException


class UserManager:
    """
    Manages user-related operations, such as authentication, adding users, and activation.
    """
    users = []

    def load_users(self):
        """
        Load users from the CSV file into a list of User objects.

        :return: List of User objects.
        """

    try:
        with open(User.users_file, mode='r') as file:
            flag = False
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if flag:
                    username , password_hash , active = row[0], row[1], str(row[2])
                    user = User(username, password_hash, active)
                    users.append(user)
                flag = True
    except FileNotFoundError:
            print("Users file not found. Starting with an empty list.")


    def save_users(self, users):
        """
        Save all users back to the CSV file.
        """
        with open(User.users_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username","Password","Active"])
            for user in users:
                writer.writerow([user.username, user.password_hash, user.active])

    def add_user(self, username, password,users):
        """
        Add a new user to the list and save to the CSV.

        :param username: The username for the new user.
        :param password: The password for the new user.
        """
        password_hash = User.hash_password(password)
        user = User(username, password_hash)
        users.append(user)
        messagebox.showinfo("Success", f"User '{username}' added successfully.")

    def authenticate(self, username, password,users):
        """
        Authenticate a user by checking the username and password.

        :param username: The username to authenticate.
        :param password: The password to authenticate.
        :return: True if authentication is successful, otherwise False.
        """
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        for user in users:
            if user.username == username and user.password_hash == password_hash:
                user.active = "Yes"
                return True
        raise AuthenticationException("Authentication failed.")
        return False

    def user_exists(self, username,users):
        """
        Check if a username already exists in the users list.

        :param username: The username to check.
        :return: True if the user exists, otherwise False.
        """
        for user in users:
            if user.username == username:
                return True
        return False

    def activate_user(self, username,users):
        """
        Activate a user by username.

        :param username: The username to activate.
        :return: True if the user was activated, otherwise False.
        """
        for user in users:
            if user.username == username:
                user.active = "Yes"
                self.save_users(self,users)
                return True
        return False

    def deactivate_user(self, username,users):
        """
        Deactivate a user by username.

        :param username: The username to deactivate.
        :return: True if the user was deactivated, otherwise False.
        """
        for user in self.users:
            if user.username == username:
                user.active = "No"
                self.save_users(self,users)
                return True
        return False


