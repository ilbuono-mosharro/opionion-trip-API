from django.db import models


class CityQuerySet(models.QuerySet):
    def cities_active(self):
        return self.filter(is_active=True).select_related('user').prefetch_related('city_images', 'city_attractions')

    def staff_cities(self, user):
        return self.filter(user=user).select_related('user')
