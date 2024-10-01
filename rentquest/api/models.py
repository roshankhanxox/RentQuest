from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("landlord", "Landlord"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class Property(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.IntegerField()  # size to be entered in square feet
    landlord = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="properties/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
