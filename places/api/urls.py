from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'attractions', views.AttractionViewSet, basename="attractions")

urlpatterns = [
    path('', include(router.urls)),
    path('image-attraction-ud/<uuid:pk>/', views.ImageAttractionUd.as_view(), name="image_attraction_ad")
]
