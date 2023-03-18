from rest_framework import viewsets, permissions, status, generics, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from reviews.api.serializers import ReviewRatingSerializer
from .serializer import AttractionsSerializer, ImageAttractionSerializer
from ..models import Attractions, ImageAttractions
from cities.api.permissions import IsOwnerOrReadOnly, IsOwner


class AttractionViewSet(viewsets.ModelViewSet):
    queryset = Attractions.objects.all()
    serializer_class = AttractionsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, ip=self.request.META.get("REMOTE_ADDR"))

    @action(detail=False, methods=['get'], url_name="get-attractions-by-user", url_path="get_attractions_by_user",
            permission_classes=[permissions.IsAuthenticated, IsOwner])
    def get_attractions_by_user(self, request, *arg, **kwargs):
        user = self.request.user
        queryset = Attractions.objects.filter(user=user)
        serializer = AttractionsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_name="get-attraction-images", url_path="get_attraction_images",
            permission_classes=[permissions.IsAuthenticated, IsOwner])
    def get_attraction_images(self, request, pk=None, *args, **kwargs):
        attraction = self.get_object()
        images = attraction.attractions_images.all()
        serializer = ImageAttractionSerializer(images, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_name="add-image-attraction", url_path="add_image_attraction",
            permission_classes=[permissions.IsAuthenticated, IsOwner])
    def add_image_attraction(self, request, pk=None, *args, **kwargs):
        attraction = self.get_object()
        serializer = ImageAttractionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, attraction=attraction, ip=self.request.META.get("REMOTE_ADDR"))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_name="add-wishlist", url_path="add_wishlist",
            permission_classes=[permissions.IsAuthenticated])
    def add_wishlist(self, request, pk=None, *arg, **kwargs):
        attraction = self.get_object()
        if attraction.users_wishlist.filter(id=self.request.user.id).exists():
            attraction.users_wishlist.remove(self.request.user)
        else:
            attraction.users_wishlist.add(self.request.user)
        serializer = self.get_serializer(attraction)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path="add-review", url_name="add_review")
    def add_review(self, request, pk=None, *args, **kwargs):
        attraction = self.get_object()
        serializer = ReviewRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, attraction=attraction, ip=self.request.META.get("REMOTE_ADDR"))
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_name="attraction-reviews", url_path="attraction_reviews")
    def attraction_reviews(self, request, pk=None, *args, **kwargs):
        attraction = self.get_object()
        queryset = attraction.review_attraction.filter(status="AP")
        serializer = ReviewRatingSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Attractions.objects.all()
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class ImageAttractionUd(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = ImageAttractions.objects.all()
    serializer_class = ImageAttractionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
