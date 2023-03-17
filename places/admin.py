from django.contrib import admin
from .models import Attractions, ImageAttractions
# Register your models here.

@admin.register(Attractions)
class AttractionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('user', 'name', 'is_active', 'ip', 'title',)
    list_filter = ('user', 'is_active', 'created_at', 'updated_at',)
    search_fields = ('title', 'description',)
    list_per_page = 20


@admin.register(ImageAttractions)
class AttractionImagesAdmin(admin.ModelAdmin):
    list_display = ('user', 'attraction', 'is_active', 'ip',)
    list_filter = ('user', 'is_active', 'created_at', 'updated_at',)
    search_fields = ('user', 'attraction',)
    list_per_page = 20