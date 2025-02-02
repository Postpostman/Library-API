from django.db import models

from books.models import Book


class Borrowing(models.Model):
    Borrow_date = models.DateField()
    Expected_return_date = models.DateField()
    Actual_return_day = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="borrowings"
    )
    is_returned = models.BooleanField(default=False)

    def str(self):
        return f"Borrowing of {self.book} by {self.customer}"