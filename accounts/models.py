import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, validate_image_file_extension, validate_ipv46_address
from django.db import models

from .utils import validate_minimum_size, validate_file_size, GenderChoices, ContryChoices


# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    filename_rename = f'{uuid.uuid4()}.{ext}'
    return '{0}/{1}_profile/{2}'.format(instance.id, str(instance.__class__.__name__).lower(), filename_rename)

# custom user model
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_confirmation = models.BooleanField(default=False)
    age = models.PositiveSmallIntegerField(default=18)
    gender = models.CharField(max_length=3, choices=GenderChoices.choices, default=GenderChoices.PREFER_NOT_TO_SAY)
    city = models.CharField(max_length=200)
    contry = models.CharField(max_length=250, choices=ContryChoices.choices)
    avatar = models.ImageField(upload_to=user_directory_path, validators=[
        validate_image_file_extension, FileExtensionValidator(['JPEG', 'JPG', 'PNG']), validate_file_size,
        validate_minimum_size], blank=True, null=True)
    terms_and_privacy = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(validators=[validate_ipv46_address], default='192.168.100.1')

    def user_reviews_number(self):
        return self.user_review.count()

    def user_reviews_active(self):
        return self.user_review.filter(status="AP").count()

    def user_wishlist_number(self):
        return self.users_wishlist.count()
