from django.db import models
from borrowing.models import Borrowing


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"


class PaymentType(models.TextChoices):
    PAYMENT = "PAYMENT", "Payment"
    FINE = "FINE", "Fine"


class Payment(models.Model):
    status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    type = models.CharField(
        max_length=10, choices=PaymentType.choices, default=PaymentType.PAYMENT
    )
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.PROTECT, related_name="payments"
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=255, unique=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status} - ${self.money_to_pay}"
