# properties/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PropertyViewSet,
    PropertyImageViewSet,
    PropertyGeoSearchView,
    PropertyDetailView,
)

router = DefaultRouter()
router.register(r"properties", PropertyViewSet)
router.register(r"property-images", PropertyImageViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("search/", PropertyGeoSearchView.as_view(), name="property-geosearch"),
    path("detail/<int:pk>/", PropertyDetailView.as_view(), name="property-detail"),
]
