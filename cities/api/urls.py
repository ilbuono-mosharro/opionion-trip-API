from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'cities', views.CityViewSet, basename="cities")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('image-city-ud/<uuid:pk>/', views.ImageUd.as_view(), name="image_city_ad")
]
