from django.db import models
from api.models import User
from cloudinary.models import CloudinaryField

# Create your models here.


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


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, related_name="property_images", on_delete=models.CASCADE
    )
    image = CloudinaryField("image")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.name}"
