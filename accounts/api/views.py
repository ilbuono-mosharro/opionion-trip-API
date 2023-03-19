from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

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


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        # Rimuovi il token dall'oggetto request dell'utente
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
