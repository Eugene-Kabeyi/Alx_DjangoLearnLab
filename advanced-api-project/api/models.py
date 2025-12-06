from django.db import models

# Author model
class Author(models.Model):
    name = models.CharField(max_length=100) # Author's name
    
    # String representation of the Author
    def __str__(self):
        return self.name

# Book model 
class Book(models.Model):
    title = models.CharField(max_length=200) # Book title
    publication_year = models.IntegerField() # Year the book was published
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books') # Link to the author
    
    # String representation of the Book
    def __str__(self):
        return self.title