from django.db import models


class Customer(models.Model):
    Email = models.CharField(max_length=50)
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)

    def str(self):
        return f"{self.First_name} {self.Last_name} ({self.Email})"