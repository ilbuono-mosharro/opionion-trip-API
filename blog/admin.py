from django.contrib import admin
from .models import Post, Comment


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status', 'publish',)
    list_filter = ('status', 'created', 'publish', 'author',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish',)


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'created', 'active',)
    list_filter = ('body', 'post',)
    search_fields = ('body',)
    raw_id_fields = ('post',)
    date_hierarchy = 'created'
    ordering = ('active',)
