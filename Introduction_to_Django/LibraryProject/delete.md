# Delete the book instance

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Delete the book safely

book = Book.objects.filter(title="Nineteen Eighty-Four").first()
if book:
book.delete()

# Confirm deletion

Book.objects.filter(title="Nineteen Eighty-Four").exists()

# Expected Output(1, {'bookshelf.Book': 1}) , False
