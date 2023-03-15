from django.contrib import sitemaps
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from cities.models import City
from places.models import Attractions


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['pages:home', 'pages:privacy', 'pages:cookie', 'pages:terms']

    def location(self, item):
        return reverse(item)


class CitySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return City.cities.cities_active()

    def lastmod(self, obj):
        return obj.updated_at


class AttractionsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Attractions.attraction.attractions_active()

    def lastmod(self, obj):
        return obj.updated_at
