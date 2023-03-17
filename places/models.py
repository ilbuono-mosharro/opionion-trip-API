import uuid

from django.conf import settings
from django.core.validators import validate_ipv46_address, validate_slug, validate_image_file_extension, \
    FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import User
from accounts.utils import validate_file_size, user_directory_path
from cities.models import City
from images.models import Image
from .custom_queryset import AttractionQuerySet


# Create your models here.
class Attractions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="city_attractions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_attractions")
    name = models.CharField(max_length=150)
    adress = models.CharField(max_length=250)
    cap = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=250, unique=True)
    description = models.TextField(max_length=900)
    slug = models.SlugField(max_length=200, validators=[validate_slug])
    is_active = models.BooleanField(default=False)
    copertina = models.ImageField(upload_to=user_directory_path,
                                  validators=[validate_image_file_extension,
                                              FileExtensionValidator(['JPEG', 'JPG', 'PNG']), validate_file_size])
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users_wishlist", blank=True)
    ip = models.GenericIPAddressField(validators=[validate_ipv46_address])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # The default manager.
    attraction = AttractionQuerySet.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Attractions, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Attraction'
        verbose_name_plural = 'Attractions'

    def get_absolute_url(self):
        return reverse('places:attraction_page', kwargs={'slug': self.slug})

    def get_wishlist_number(self):
        return self.users_wishlist.count()


class ImageAttractions(Image):
    attraction = models.ForeignKey(Attractions, on_delete=models.CASCADE, related_name="attractions_images")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_images_attractions')
    image = models.ImageField(upload_to=user_directory_path,
                              validators=[validate_image_file_extension,
                                          FileExtensionValidator(['JPEG', 'JPG', 'PNG']), validate_file_size])
