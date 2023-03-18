import uuid
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.core.validators import MaxValueValidator, validate_ipv46_address, MinValueValidator
from django.db import models
from places.models import Attractions
from .custom_queryset import UserReviewsQuerySet


# Create your models here.
class ReviewRating(models.Model):
    class ReviewStatus(models.TextChoices):
        APPROVED = 'AP', _('Approved')
        REJECT = 'RE', _('Reject')
        WAITING = 'WA', _('Waiting')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attraction = models.ForeignKey(Attractions, on_delete=models.CASCADE, related_name='review_attraction')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_review')
    subject = models.CharField(max_length=100)
    review = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    users_vote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users_vote", blank=True)
    ip = models.GenericIPAddressField(validators=[validate_ipv46_address])
    status = models.CharField(max_length=8, choices=ReviewStatus.choices, default=ReviewStatus.WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # The default manager.
    user_reviews = UserReviewsQuerySet.as_manager()

    def __str__(self):
        return self.subject

    def total_vote(self):
        return self.users_vote.count()

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ('-created_at',)


class ReportReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_report_review')
    review = models.ForeignKey(ReviewRating, on_delete=models.CASCADE, related_name='review_report')
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    ip = models.GenericIPAddressField(validators=[validate_ipv46_address])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Report Review"
        verbose_name_plural = "Reports Reviews"
        ordering = ('-created_at',)
