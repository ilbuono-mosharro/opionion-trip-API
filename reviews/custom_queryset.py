from django.db import models


class UserReviewsQuerySet(models.QuerySet):
    def reviews_waiting(self):
        return self.filter(status="WA").select_related('attraction', 'user').prefetch_related(
            'users_vote', 'review_report')

    def reviews_approved(self):
        return self.filter(status="AP").select_related('attraction', 'user').prefetch_related(
            'users_vote', 'review_report')

    def user_reviews_query(self, user):
        return self.filter(user=user).select_related('attraction', 'user')

    def reviews_staff_admin_check(self):
        return self.all().select_related('attraction', 'user')
