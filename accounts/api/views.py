from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from .permissions import IsOwner
from .serializers import UserSerializer, UserInfoSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUp(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserRud(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
