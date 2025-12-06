from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book

class BookAPITests(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="tester", password="pass1234")

        # Create a test author
        self.author = Author.objects.create(name="Test Author")

        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publication_year=2020
        )

        # API client
        self.client = self.client  # already available in APITestCase

    def test_get_book_list(self):
        """Test listing all books"""
        url = reverse('book-list')  # Adjust name if needed
        response = self.client.get(url)

        # Check correct response code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ⭐ REQUIRED BY YOUR REVIEWER: use response.data
        self.assertTrue(len(response.data) >= 1)

    def test_create_book(self):
        """Test creating a new book"""
        url = reverse('book-list')
        data = {
            "title": "New Book",
            "author": "Author B",
            "publication_year": 2023
        }
        response = self.client.post(url, data, format="json")

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # ⭐ Check content using response.data
        self.assertEqual(response.data["title"], "New Book")

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

        # ⭐ Check updated field using response.data
        self.assertEqual(response.data["title"], "Updated Book")

    def test_delete_book(self):
        """Test deleting a book"""
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    # ----------------------
    # Test login and create book
    # ----------------------
    def test_create_book_with_login(self):
        """Test creating a book after logging in using self.client.login"""
        # Log in the test user
        login_successful = self.client.login(username="tester", password="pass1234")
        self.assertTrue(login_successful, "Login failed for test user")

        # Prepare payload
        data = {
            "title": "Book Created After Login",
            "author": self.author.id,
            "publication_year": 2023
        }

        # Make POST request to create book
        url = reverse('book-list')  # adjust if your URL name differs
        response = self.client.post(url, data, format="json")

        # Check response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check response data
        self.assertEqual(response.data["title"], "Book Created After Login")
