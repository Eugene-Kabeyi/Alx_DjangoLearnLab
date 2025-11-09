book = Book.objects.filter(title="1984")
if book:
book.title = "Nineteen Eighty-Four"
book.save()
book.title

# Expected Output'Nineteen Eighty-Four'
