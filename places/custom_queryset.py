from django.db import models
from django.db.models import Count, Q, Avg, FloatField


class AttractionQuerySet(models.QuerySet):
    def attractions_active(self):
        return self.select_related('city', 'user').prefetch_related(
            'users_wishlist', 'attractions_images', 'review_attraction'
        ).filter(is_active=True).annotate(
            review_number=Count('review_attraction', filter=Q(review_attraction__status="AP")),
            review_avg=Avg('review_attraction__rating', filter=Q(review_attraction__status="AP"),
                           output_field=FloatField()),
            review_5=Count('review_attraction__rating', filter=Q(review_attraction__status="AP",
                                                                 review_attraction__rating=5)),
            review_4=Count('review_attraction__rating', filter=Q(review_attraction__status="AP",
                                                                 review_attraction__rating=4)),
            review_3=Count('review_attraction__rating', filter=Q(review_attraction__status="AP",
                                                                 review_attraction__rating=3)),
            review_2=Count('review_attraction__rating', filter=Q(review_attraction__status="AP",
                                                                 review_attraction__rating=2)),
            review_1=Count('review_attraction__rating', filter=Q(review_attraction__status="AP",
                                                                 review_attraction__rating=1)),
        )

    def wishlist_user(self, wishlist):
        return self.select_related('city', 'user').prefetch_related(
            'users_wishlist'
        ).filter(users_wishlist=wishlist)

    def staff_attractions(self, user):
        return self.select_related('city', 'user').prefetch_related(
            'users_wishlist'
        ).filter(user=user)
