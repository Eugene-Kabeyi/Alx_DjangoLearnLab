# Import all your models
from relationship_app.models import Author, Book, Library, Librarian

# -----------------------------------------
# 1. Query all books by a specific author
# -----------------------------------------

author_name = "George Orwell"
author = Author.objects.filter(name=author_name).first()

print("\n Books by", author_name + ":")
if author:
    books = author.books.all()
    for book in books:
        print(" -", book.title)
else:
    print("Author not found!")

# -----------------------------------------
# 2. List all books in a library
# -----------------------------------------

library_name = "Central Library"
library = Library.objects.filter(name=library_name).first()

print("\n Books in", library_name + ":")
if library:
    for book in library.books.all():
        print(" -", book.title)
else:
    print("Library not found!")

# -----------------------------------------
# 3. Retrieve the librarian for a library
# -----------------------------------------

print("\n Librarian for", library_name + ":")
if library and hasattr(library, 'librarian'):
    print(" -", library.librarian.name)
else:
    print("No librarian assigned or library not found!")
