# Import all your models
from relationship_app.models import Author, Book, Library, Librarian

# -----------------------------------------
# 1. Query all books by a specific author
# -----------------------------------------

author_name = "George Orwell"

try:
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)  # Instead of author.books.all()
    
    print("\nBooks by", author_name + ":")
    for book in books:
        print(" -", book.title)
except Author.DoesNotExist:
    print("Author not found!")


# -----------------------------------------
# 2. List all books in a library (using .get)
# -----------------------------------------

library_name = "Central Library"

print("\n Books in", library_name + ":")
try:
    library = Library.objects.get(name=library_name)
    for book in library.books.all():
        print(" -", book.title)
except Library.DoesNotExist:
    print("Library not found!")


# -----------------------------------------
# 3. Retrieve the librarian for a library
# -----------------------------------------

print("\n Librarian for", library_name + ":")
if library and hasattr(library, 'librarian'):
    print(" -", library.librarian.name)
else:
    print("No librarian assigned or library not found!")
