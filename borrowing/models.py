from django.db import models

from books.models import Book
from customer.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_day = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrowings"
    )
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Borrowing of {self.book} by {self.user}"