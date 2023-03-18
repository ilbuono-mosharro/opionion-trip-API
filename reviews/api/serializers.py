from rest_framework import serializers
from ..models import ReviewRating, ReportReview
from accounts.api.serializers import UserInfoSerializer
from places.api.serializer import AttractionsSerializer


class ReviewRatingSerializer(serializers.ModelSerializer):
    attraction = AttractionsSerializer(read_only=True)
    user = UserInfoSerializer(read_only=True)
    users_vote = UserInfoSerializer(read_only=True, many=True)

    class Meta:
        model = ReviewRating
        fields = ['attraction', 'user', 'subject', 'review', 'rating', 'users_vote', 'ip', 'status', 'created_at']
        read_only_fields = ['ip', 'status', 'created_at']

    def create(self, validated_data):
        return ReviewRating.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.subject = validated_data.get('subject', instance.subject)
        instance.review = validated_data.get('review', instance.review)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

class ReportReviewSerializer(serializers.ModelSerializer):
    review = ReviewRatingSerializer(read_only=True)
    user = UserInfoSerializer(read_only=True)
    class Meta:
        model = ReportReview
        fields = ['user', 'review', 'subject', 'description', 'ip', 'created_at']
        read_only_fields = ['ip', 'created_at']

    def create(self, validated_data):
        return ReportReview.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.subject = validated_data.get('subject', instance.subject)
        instance.review = validated_data.get('review', instance.review)
        instance.save()
        return instance
