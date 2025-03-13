from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book
from django.urls import reverse

BOOKS_URL = reverse("books:books-list")


def detail_url(book_id):
    return reverse("books:books-detail", args=[book_id])


class PublicBookApiTests(TestCase):
    """Test for public permission to books API"""

    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=1.99
        )

    def test_list_books(self):
        """Test views books API"""
        res = self.client.get(BOOKS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("title", res.data[0])

    def test_retrieve_book(self):
        """Test view specific book"""
        res = self.client.get(detail_url(self.book.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], self.book.title)

    def test_create_book_forbidden(self):
        """Test for banning the creation of a book by an unauthorized user"""
        payload = {
            "title": "New Book",
            "author": "New Author",
            "cover": "HARD",
            "inventory": 3,
            "daily_fee": 2.50
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    """Tests for administrative access to the books API"""

    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="password123"
        )
        self.client.force_authenticate(self.admin_user)

    def test_create_book(self):
        """Book creation test by the administrator"""
        payload = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 4,
            "daily_fee": 3.00
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().title, payload["title"])

    def test_update_book(self):
        """Book update test by the administrator"""
        book = Book.objects.create(
            title="Old Title",
            author="Old Author",
            cover=Book.CoverType.HARD,
            inventory=2,
            daily_fee=1.50
        )
        payload = {"title": "Updated Title"}
        res = self.client.patch(detail_url(book.id), payload)
        book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(book.title, payload["title"])

    def test_delete_book(self):
        """Test of deleting a book by an administrator"""
        book = Book.objects.create(
            title="To Delete",
            author="Some Author",
            cover=Book.CoverType.SOFT,
            inventory=1,
            daily_fee=2.00
        )
        res = self.client.delete(detail_url(book.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())
