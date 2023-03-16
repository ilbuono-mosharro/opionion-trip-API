from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CitySerializer, ImageCitySerializer
from ..models import City, ImageCity
from rest_framework import viewsets, permissions, status, generics, mixins
from .permissions import IsOwnerOrReadOnly, IsOwner


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_name="get-cities-by-user", url_path="get_cities_by_user",
            permission_classes=[permissions.IsAuthenticated, IsOwner])
    def get_cities_by_user(self, request, *arg, **kwargs):
        user = request.user
        queryset = City.objects.filter(user=user)
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_name="get-city-images", url_path="get_city_images",
            permission_classes=[permissions.IsAuthenticated, IsOwner])
    def get_city_images(self, request, pk=None, *args, **kwargs):
        city = self.get_object()
        images = city.city_images.all()
        serializer = ImageCitySerializer(images, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_name="add-image", url_path="add_image",
            permission_classes=[permissions.IsAuthenticated, IsOwner])
    def add_image(self, request, pk=None, *args, **kwargs):
        city = self.get_object()
        serializer = ImageCitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, city=city, ip=self.request.META.get("REMOTE_ADDR"))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageUd(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = ImageCity.objects.all()
    serializer_class = ImageCitySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
