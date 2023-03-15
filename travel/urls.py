"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

from accounts.forms import EmailValidationOnForgotPassword
from .sitemaps import StaticViewSitemap, CitySitemap, AttractionsSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'cities': CitySitemap,
    'attractions': AttractionsSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='registration')),
    path('', include('pages.urls', namespace='pages')),
    path('', include('cities.urls', namespace='cities')),
    path('', include('places.urls', namespace='places')),
    path('', include('search.urls', namespace='search')),
    path('', include('reviews.urls', namespace='reviews')),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword),
         name='password_reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^robots\.txt', include('robots.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-blog/', include('blog.api.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)
