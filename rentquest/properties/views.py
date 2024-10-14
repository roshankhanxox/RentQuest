from rest_framework import viewsets, permissions, status, generics
from django.db.models import Q
from django.conf import settings
from geopy.geocoders import GoogleV3
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Property, PropertyImage
from .serializers import PropertySerializer, PropertyImageSerializer
from math import radians, sin, cos, sqrt, atan2


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "landlord":
            raise PermissionDenied("Only landlords can create property")
        property_instance = serializer.save(landlord=self.request.user)
        return Response(
            {"message": "Property created successfully", "id": property_instance.id},
            status=status.HTTP_201_CREATED,
        )

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


class PropertyGeoSearchView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        query = self.request.query_params.get("query", None)
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        min_size = self.request.query_params.get("min_size", None)
        max_size = self.request.query_params.get("max_size", None)

        properties = Property.objects.all()

        if query:
            # Geocode the location to get latitude and longitude
            geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
            location = geolocator.geocode(query)

            if location:
                lat = location.latitude
                lng = location.longitude

                # Filter properties based on the latitude and longitude
                properties = properties.filter(
                    Q(latitude__isnull=False, longitude__isnull=False)
                )

                # Apply distance filtering
                nearby_properties = []
                for property in properties:
                    distance = self.calculate_distance(
                        lat, lng, property.latitude, property.longitude
                    )
                    if distance <= 5:  # Assuming 5 km radius
                        nearby_properties.append(property)

                properties = nearby_properties

        # Apply additional filters if specified
        if min_price:
            properties = [prop for prop in properties if prop.price >= float(min_price)]
        if max_price:
            properties = [prop for prop in properties if prop.price <= float(max_price)]
        if min_size:
            properties = [prop for prop in properties if prop.size >= int(min_size)]
        if max_size:
            properties = [prop for prop in properties if prop.size <= int(max_size)]

        return properties

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Convert Decimal to float
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)

        # Haversine formula to calculate the distance
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = (
            sin(dlat / 2) ** 2
            + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        )
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6371 * c  # Radius of Earth in kilometers
        return distance


# class PropertyGeoSearchView(generics.ListAPIView):
#     serializer_class = PropertySerializer

#     def get_queryset(self):
#         query = self.request.query_params.get("query", None)

#         if query:
#             # Geocode the location to get latitude and longitude
#             geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
#             location = geolocator.geocode(query)

#             if location:
#                 lat = location.latitude
#                 lng = location.longitude

#                 # Filter properties based on the latitude and longitude
#                 # You may need to implement a distance calculation to filter results based on distance
#                 properties = Property.objects.filter(
#                     Q(latitude__isnull=False, longitude__isnull=False)
#                 )

#                 # Example of filtering properties within a certain distance (e.g., 5km)
#                 # This assumes you have a method to calculate distance
#                 # You can also refine this to include a more sophisticated approach using haversine formula
#                 nearby_properties = []
#                 for property in properties:
#                     # Calculate distance (using haversine or another method)
#                     distance = self.calculate_distance(
#                         lat, lng, property.latitude, property.longitude
#                     )
#                     if distance <= 5:  # Assuming 5 km radius
#                         nearby_properties.append(property)

#                 return nearby_properties

#         # Return all properties if no query is provided or geocoding fails
#         return Property.objects.all()

#     def calculate_distance(self, lat1, lon1, lat2, lon2):
#         # Convert Decimal to float
#         lat1 = float(lat1)
#         lon1 = float(lon1)
#         lat2 = float(lat2)
#         lon2 = float(lon2)

#         # Haversine formula to calculate the distance
#         dlat = radians(lat2 - lat1)
#         dlon = radians(lon2 - lon1)
#         a = (
#             sin(dlat / 2) ** 2
#             + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
#         )
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#         distance = 6371 * c  # Radius of Earth in kilometers
#         return distance


# class PropertyGeoSearchView(generics.ListAPIView):
#     serializer_class = PropertySerializer

#     def get_queryset(self):
#         query = self.request.query_params.get("query", None)
#         min_price = self.request.query_params.get("min_price", None)
#         max_price = self.request.query_params.get("max_price", None)
#         min_size = self.request.query_params.get("min_size", None)
#         max_size = self.request.query_params.get("max_size", None)

#         if query:
#             # Geocode the location to get latitude and longitude
#             geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
#             location = geolocator.geocode(query)

#             if location:
#                 lat = location.latitude
#                 lng = location.longitude

#                 # Filter properties based on the latitude and longitude
#                 properties = Property.objects.filter(
#                     Q(latitude__isnull=False, longitude__isnull=False)
#                 )

#                 # Filter by distance
#                 nearby_properties = []
#                 for property in properties:
#                     distance = self.calculate_distance(
#                         lat, lng, property.latitude, property.longitude
#                     )
#                     if distance <= 5:  # Assuming 5 km radius
#                         nearby_properties.append(property)

#                 properties = nearby_properties  # Update the properties list

#         else:
#             properties = Property.objects.all()

#         # Apply additional filters if specified
#         if min_price:
#             properties = [prop for prop in properties if prop.price >= float(min_price)]
#         if max_price:
#             properties = [prop for prop in properties if prop.price <= float(max_price)]
#         if min_size:
#             properties = [prop for prop in properties if prop.size >= int(min_size)]
#         if max_size:
#             properties = [prop for prop in properties if prop.size <= int(max_size)]

#         return properties

#     def calculate_distance(self, lat1, lon1, lat2, lon2):
#         # Convert Decimal to float
#         lat1 = float(lat1)
#         lon1 = float(lon1)
#         lat2 = float(lat2)
#         lon2 = float(lon2)

#         # Haversine formula to calculate the distance
#         dlat = radians(lat2 - lat1)
#         dlon = radians(lon2 - lon1)
#         a = (
#             sin(dlat / 2) ** 2
#             + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
#         )
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#         distance = 6371 * c  # Radius of Earth in kilometers
#         return distance
