from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Property, PropertyImage
from .serializers import PropertySerializer, PropertyImageSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "landlord":
            raise PermissionDenied("Only landlords can create property")
        serializer.save(landlord=self.request.user)

    def get_queryset(self):
        return Property.objects.filter(landlord=self.request.user)


class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        property_id = self.request.data.get("property_id")
        property_instance = Property.objects.get(id=property_id)
        if property_instance.landlord != self.request.user:
            raise PermissionDenied(
                "You can only upload images for your own properties."
            )
        serializer.save(property=property_instance)
