from django.contrib import admin
from .models import City, ImageCity
# Register your models here.


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('user', 'name', 'is_active', 'ip', 'title',)
    list_filter = ('user', 'is_active', 'created_at', 'updated_at',)
    search_fields = ('title', 'description',)
    list_per_page = 20


@admin.register(ImageCity)
class CityImagesAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'is_active', 'ip',)
    list_filter = ('user', 'is_active', 'created_at', 'updated_at',)
    search_fields = ('user', 'city',)
    list_per_page = 20