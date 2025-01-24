from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    Title = models.CharField(max_length=63)
    Author = models.CharField(max_length=50)
    Cover = models.CharField(
        max_length=5,
        choices=CoverType.choices,
        default=CoverType.HARD,
    )
    Inventory = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    Daily_fee = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.01)],
    )

    def __str__(self):
        return f"{self.Title} by {self.Author}"


class Customer(models.Model):
    Email = models.CharField(max_length=50)
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.First_name} {self.Last_name} ({self.Email})"


class Borrowing(models.Model):
    Borrow_date = models.DateField()
    Expected_return_date = models.DateField()
    Actual_return_day = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="borrowings"
    )
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Borrowing of {self.book} by {self.customer}"
