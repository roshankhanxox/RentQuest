from rest_framework import serializers
from .models import User, Property


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            "id",
            "name",
            "location",
            "price",
            "size",
            "landlord",
            "images",
            "created_at",
        ]
