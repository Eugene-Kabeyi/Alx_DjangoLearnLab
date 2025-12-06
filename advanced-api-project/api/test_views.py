from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book

class BookAPITests(APITestCase):

    def setUp(self):
        # Create a book before each test
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            publication_year=2020
        )

    def test_get_book_list(self):
        """Test listing all books"""
        url = reverse('book-list')  # Adjust name based on your urls
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        """Test creating a new book"""
        url = reverse('book-list')
        data = {
            "title": "New Book",
            "author": "Author B",
            "publication_year": 2023
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        """Test updating a book"""
        url = reverse('book-detail', args=[self.book.id])
        data = {
            "title": "Updated Book",
            "author": "John Doe",
            "publication_year": 2021
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        """Test deleting a book"""
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
