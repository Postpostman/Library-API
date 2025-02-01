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
