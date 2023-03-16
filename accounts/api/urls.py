from django.urls import path
from . import views

urlpatterns = [
    path("sign-up/", views.SignUp.as_view(), name="sign-up"),
    path("user/<uuid:pk>/", views.UserRud.as_view(), name="user-rud"),
]
