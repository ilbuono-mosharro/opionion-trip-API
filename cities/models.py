import uuid

from django.conf import settings
from django.utils.text import slugify
from accounts.models import User
from django.core.validators import validate_ipv46_address, validate_image_file_extension, FileExtensionValidator, \
    validate_slug
from django.db import models
from django.urls import reverse

from accounts.utils import validate_file_size, user_directory_path
from images.models import Image
from .custom_queryset import CityQuerySet


# Create your models here.
class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_city')
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=250, unique=True)
    description = models.TextField(max_length=900)
    slug = models.SlugField(max_length=200, validators=[validate_slug])
    is_active = models.BooleanField(default=False)
    copertina = models.ImageField(upload_to=user_directory_path, validators=[
        validate_image_file_extension, FileExtensionValidator(['JPEG', 'JPG', 'PNG']), validate_file_size
    ])
    ip = models.GenericIPAddressField(validators=[validate_ipv46_address])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # The default manager.
    cities = CityQuerySet.as_manager()

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ('name',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cities:city_page', kwargs={'slug': self.slug})

    def get_number_attractions(self):
        return self.city_attractions.count()


class ImageCity(Image):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="city_images")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_images_city')
    image = models.ImageField(upload_to=user_directory_path, validators=[
        validate_image_file_extension, FileExtensionValidator(['JPEG', 'JPG', 'PNG']), validate_file_size
    ])
