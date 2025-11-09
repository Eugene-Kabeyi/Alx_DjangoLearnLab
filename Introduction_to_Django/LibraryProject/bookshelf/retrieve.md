# Retrieve the book using get() safely by including author
book = Book.objects.get(title="1984", author="George Orwell")
book.title, book.author, book.publication_year


# Expected Output : ('1984', 'George Orwel', 1949)
