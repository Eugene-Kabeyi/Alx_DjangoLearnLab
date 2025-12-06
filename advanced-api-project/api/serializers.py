from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# ==========================
# Book Serializer
# ==========================
# This serializer converts Book model instances to JSON,
# and also handles validations when creating new Book objects.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # Serialize all fields of Book model

    # Custom validation for publication_year   
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    # This field automatically serializes all books related to the author
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['name', 'books']  # Include author's name and their books