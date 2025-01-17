
# Library Management System

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Credits](#credits)

---

## Introduction

The **Library Management System** is a Python-based application designed to simplify the management of books, users, and waitlists. It uses Object-Oriented Programming (OOP) principles with **Tkinter** for the GUI, allowing librarians and administrators to manage book inventory, user accounts, and borrowing activity efficiently.

---

## Features

### User Management
- Add new users and register them securely.
- Authenticate users using hashed passwords.
- Activate or deactivate user accounts.
- Delete users from the system.

### Book Management
- Add, edit, and delete books from the inventory.
- Search for books using various strategies (by title, author, genre, or year).
- Sort books by title, author, genre, or year.
- Lend and return books, updating available copies dynamically.
- Prevent deletion of loaned books.

### Waitlist Management
- Manage waitlists for books that are fully loaned out.
- Notify librarians when books are returned and assigned to waitlisted users.

### Advanced Patterns
- **Strategy Pattern** for implementing flexible search strategies.
- **Observer Pattern** for librarian notifications.
- **Decorator Pattern** for logging activity in the system.
- **Iterator Pattern** for traversing collections like books and users.

### Logging and Error Handling
- Centralized logging for tracking system activities.
- Custom exception handling for user input and field validation errors.

---

## Project Structure

```
OOP_3/
│
├── All_Windows/
│   ├── All_books.py        # GUI for managing and displaying books
│   ├── Book_window.py      # GUI for adding new books
│   ├── Gui_Lib.py          # Shared GUI utilities
│   ├── Library_System.py   # Main entry point for the system
│   ├── Login_window.py     # GUI for user login
│   ├── Register.py         # GUI for user registration
│   ├── books.csv               # CSV file for storing book inventory
│   ├── users.csv               # CSV file for storing user accounts
│   ├── Waitlist.csv            # CSV file for managing waitlists
│
├── Backend/
│   ├── Book.py             # Book object and related logic
│   ├── BookManager.py      # Manage books and inventory
│   ├── LibrarianObserver.py# Notifications for librarians
│   ├── Logger.py           # Logging utilities
│   ├── Strategy_Search.py  # Search strategies (Strategy Pattern)
│   ├── User.py             # User object and related logic
│   ├── UserManager.py      # Manage user authentication and accounts
│   ├── WaitlistManager.py  # Manage waitlists for loaned books
│
├── Exceptions/
│   ├── BaseException.py    # Base exception class
│   ├── FieldException.py   # Handles field-related exceptions
│   ├── UserException.py    # Handles user-related exceptions
│
├── tests/                  # Unit tests for all components
│   ├── test_BookManager.py
│   ├── test_UserManager.py
│   ├── test_WaitlistManager.py
│   ├── test_Strategy_Search.py
│   ├── test_LibrarianObserver.py
│   ├── test_Logger.py
│
├── books.csv               # CSV file for storing book inventory
├── users.csv               # CSV file for storing user accounts
├── Waitlist.csv            # CSV file for managing waitlists
├── README.md               # Project documentation
```

---

## Installation

### Prerequisites
1. Python 3.8+ installed on your system.
2. Install required dependencies using `pip`.

4. Run the main system:
   ```bash
   python All_Windows/Gui_Lib
   ```

---

## Usage

1. **Start the Application**:
   - Run `Gui_Lib` to launch the application.
2. **Login**:
   - Login with existing credentials or register a new account.
3. **Manage Books**:
   - Add, delete, lend, return, or search for books using the `All Books` interface.
4. **Manage Users**:
   - Add, activate, deactivate, or delete users from the system.
5. **Manage Waitlists**:
   - Add customers to the waitlist for unavailable books.

---

## Testing

Tests cover:
- BookManager functionality (add, remove, search, etc.).
- UserManager functionality (authentication, activation, etc.).
- WaitlistManager operations.
- Search strategies.
- Logging and notifications.

---

## Technologies Used

- **Python**: Core programming language.
- **Tkinter**: For the graphical user interface (GUI).
- **unittest**: Built-in Python library for testing.
- **mock**: To mock dependencies and isolate tests.
- **CSV**: For data persistence (books, users, waitlists).

---
