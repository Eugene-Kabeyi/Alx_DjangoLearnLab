# api/test_views.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Author


class BookAPITests(TestCase):

    # This function runs before every test
    def setUp(self):
        # Create a test author
        self.author = Author.objects.create(name="Test Author")

        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            description="A simple test book",
            author=self.author
        )

        # Create client to simulate API calls
        self.client = APIClient()

    # -----------------------------
    # 📌 TEST LIST BOOK ENDPOINT
    # -----------------------------
    def test_book_list(self):
        response = self.client.get("/books/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -----------------------------
    # 📌 TEST BOOK DETAIL ENDPOINT
    # -----------------------------
    def test_book_detail(self):
        response = self.client.get(f"/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -----------------------------
    # 📌 TEST CREATE BOOK ENDPOINT
    # -----------------------------
    def test_create_book(self):
        data = {
            "title": "New Book",
            "description": "New desc",
            "author": self.author.id
        }

        response = self.client.post("/books/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # -----------------------------
    # 📌 TEST UPDATE BOOK ENDPOINT
    # -----------------------------
    def test_update_book(self):
        data = {
            "title": "Updated Title",
            "description": "Updated description",
            "author": self.author.id
        }

        response = self.client.put(f"/books/update/?id={self.book.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -----------------------------
    # 📌 TEST DELETE BOOK ENDPOINT
    # -----------------------------
    def test_delete_book(self):
        response = self.client.delete(f"/books/delete/?id={self.book.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
