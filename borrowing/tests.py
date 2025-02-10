from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book
from borrowing.models import Borrowing
from django.urls import reverse
from django.utils.timezone import now

BORROWING_URL = reverse("borrowing-list")


def detail_url(borrowing_id):
    return reverse("borrowing-detail", args=[borrowing_id])


class PublicBorrowingApiTests(TestCase):
    """Tests for public access to borrowing API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required for borrowing API"""
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBorrowingApiTests(TestCase):
    """Tests for authenticated users accessing the borrowing API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="password123"
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowings(self):
        """Test retrieving a list of borrowings for an authenticated user"""
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_borrowing(self):
        """Test creating a new borrowing"""
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=1.99
        )
        payload = {
            "borrow_date": now().date(),
            "expected_return_date": now().date(),
            "book": book.id
        }
        res = self.client.post(BORROWING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.get(id=book.id).inventory, 4)

    def test_return_borrowing(self):
        """Test returning a borrowed book"""
        book = Book.objects.create(
            title="Return Test Book",
            author="Test Author",
            cover=Book.CoverType.SOFT,
            inventory=3,
            daily_fee=2.50
        )
        borrowing = Borrowing.objects.create(
            borrow_date=now().date(),
            expected_return_date=now().date(),
            actual_return_day=None,
            book=book,
            user=self.user,
            is_returned=False
        )
        url = reverse("borrowing-return-borrowing", args=[borrowing.id])
        res = self.client.post(url)
        borrowing.refresh_from_db()
        book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(borrowing.is_returned)
        self.assertEqual(book.inventory, 4)
