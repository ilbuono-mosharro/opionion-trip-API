from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from cities.api.permissions import IsOwner
from .serializers import ReviewRatingSerializer, ReportReviewSerializer
from ..models import ReviewRating


class ReviewRatingList(generics.ListAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return ReviewRating.objects.filter(user=self.request.user)


class ReviewRatingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class AddOrRemoveVote(generics.CreateAPIView):
    serializer_class = ReportReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, pk=None, *args, **kwargs):
        rating = get_object_or_404(ReviewRating, id=pk)
        if rating.users_vote.filter(id=request.user.id).exists():
            rating.users_vote.remove(self.request.user)
        else:
            rating.users_vote.add(self.request.user)
        serializer = ReviewRatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReportReviewCreate(generics.CreateAPIView):
    serializer_class = ReportReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, pk=None, *args, **kwargs):
        rating = get_object_or_404(ReviewRating, id=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, review=rating, ip=self.request.META.get('REMOTE_ADDR'))
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
