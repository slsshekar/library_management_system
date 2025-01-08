# src/library.py
import json

class Library:
    def __init__(self, library_file='library.json'):
        self.library_file = library_file
        self.books = self.load_books()

    def load_books(self):
        try:
            with open(self.library_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def add_book(self, title, author, isbn):
        book = {"title": title, "author": author, "isbn": isbn}
        self.books.append(book)
        self.save_books()

    def save_books(self):
        with open(self.library_file, 'w') as file:
            json.dump(self.books, file)
