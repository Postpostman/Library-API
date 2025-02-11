from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from borrowing.models import Borrowing
from books.models import Book
from payment.models import Payment, PaymentStatus, PaymentType
from django.utils.timezone import now

PAYMENT_URL = reverse("payment:payment-list")


def detail_url(payment_id):
    return reverse("payment:payment-detail", args=[payment_id])


class PublicPaymentApiTests(TestCase):
    """Tests for public access to payment API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required for payment API"""
        res = self.client.get(PAYMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePaymentApiTests(TestCase):
    """Tests for authenticated users accessing the payment API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="password123"
        )
        self.client.force_authenticate(self.user)

    def test_list_payments(self):
        """Test retrieving a list of payments for an authenticated user"""
        res = self.client.get(PAYMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_payment_detail(self):
        """Test retrieving payment details"""
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=1.99
        )
        borrowing = Borrowing.objects.create(
            borrow_date=now().date(),
            expected_return_date=now().date(),
            book=book,
            user=self.user,
            is_returned=False
        )
        payment = Payment.objects.create(
            status=PaymentStatus.PENDING,
            type=PaymentType.PAYMENT,
            borrowing=borrowing,
            session_url="https://payment.example.com",
            session_id="123456789",
            money_to_pay=10.00
        )
        url = detail_url(payment.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], payment.id)
        self.assertEqual(res.data["money_to_pay"], str(payment.money_to_pay))
