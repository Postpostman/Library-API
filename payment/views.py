from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from .models import Payment
from .serializers import PaymentSerializer
from .permissions import IsAdminOrOwner
from borrowing.models import Borrowing

stripe.api_key = settings.STRIPE_SECRET_KEY  # API-ключ із .env

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "type"]

    def get_queryset(self):
        """Admin can see all payments, user can only see their own"""
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing__user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create Stripe Checkout Session and payment"""
        borrowing_id = request.data.get("borrowing")
        try:
            borrowing = Borrowing.objects.get(id=borrowing_id)
        except Borrowing.DoesNotExist:
            return Response({"error": "Borrowing not found"}, status=status.HTTP_404_NOT_FOUND)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": borrowing.book.title},
                        "unit_amount": int(borrowing.book.price * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{settings.SITE_URL}/api/payments/success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.SITE_URL}/api/payments/cancel/",
        )

        payment = Payment.objects.create(
            borrowing=borrowing,
            session_id=checkout_session.id,
            session_url=checkout_session.url,
            money_to_pay=borrowing.book.price,
        )

        return Response(
            {"checkout_url": checkout_session.url},
            status=status.HTTP_201_CREATED
        )
