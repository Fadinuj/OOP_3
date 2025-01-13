from Book import Book
from BookManager import BookManager
class BookFactory(object):
    @staticmethod
    def create(title:str, author:str, copies, genre, year):
        book = Book(title, author, copies, genre, year)
        BookManager.books.append(book)