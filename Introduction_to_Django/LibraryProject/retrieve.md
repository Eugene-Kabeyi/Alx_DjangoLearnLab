book = Book.objects.filter(title="1984").first()
if book:
    book.title, book.author, book.publication_year
else:
    "No book found"

# Expected Output : ('1984', 'George Orwel', 1949)
