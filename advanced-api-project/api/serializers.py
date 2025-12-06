from rest_framework import serializers
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from .models import Author, Book
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny

# ==========================
# Book Serializer
# ==========================
# This serializer converts Book model instances to JSON,
# and also handles validations when creating new Book objects.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # Serialize all fields of Book model

    # #Create method to handle new Book instance creation
    # def create(self, validated_data):
    #     return Book.objects.create(**validated_data)
    
    
    # Custom validation for publication_year   
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.") # Throws error if year is invalid
        return value


# ===========================
# 1. LIST VIEW (GET all books)
# ===========================
# This view returns all books. Anyone can see the list.
class BookListView(ListAPIView):
    queryset = Book.objects.all()        # Fetch all books from the database
    serializer_class = BookSerializer    # Tell DRF how to convert book → JSON
    permission_classes = [AllowAny]      # No login required



# =========================================
# 2. RETRIEVE VIEW (GET a single book by id)
# =========================================
# This view returns ONE book using its primary key (pk)
class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]      # Anyone can view book details



# =============================
# 3. CREATE VIEW (POST new book)
# =============================
# This view creates a new book.
# Only logged-in users should create books.
class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]   # Must be logged in!

    # This lets us customize how a book is saved
    def perform_create(self, serializer):
        # This simply saves the book (beginner level)
        serializer.save()



# ===============================
# 4. UPDATE VIEW (PUT/PATCH book)
# ===============================
class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()  # Simple beginner save



# ============================
# 5. DELETE VIEW (DELETE book)
# ============================
class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class AuthorSerializer(serializers.ModelSerializer):
    # This field automatically serializes all books related to the author
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['name', 'books']  # Include author's name and their books
        
    # # Create method to handle new Author instance creation
    # def create(self, validated_data):
    #     return Author.objects.create(**validated_data)