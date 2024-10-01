from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PropertyViewSet

router = (
    DefaultRouter()
)  # router automaticall generates your basic urls so like /api/ or /api/users/
router.register(r"users", UserViewSet)
router.register(r"properties", PropertyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
