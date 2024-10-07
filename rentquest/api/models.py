from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


# class User(AbstractUser):
#     ROLE_CHOICES = [
#         ("student", "Student"),
#         ("landlord", "Landlord"),
#     ]
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True)
#     verification_token = models.UUIDField(
#         default=uuid.uuid4, editable=False, unique=True
#     )
#     is_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return self.username

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("landlord", "Landlord"),
    ]

    # Ensuring that role is mandatory and can't be null
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, null=False, default="student"
    )

    # UUIDField ensures unique verification token
    verification_token = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )

    is_verified = models.BooleanField(default=False)

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
