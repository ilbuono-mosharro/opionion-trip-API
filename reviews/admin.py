from django.contrib import admin
from .models import ReviewRating, ReportReview


# Register your models here.


@admin.register(ReviewRating)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'attraction', 'rating', 'status', 'ip', 'subject',)
    list_filter = ('user', 'status', 'created_at', 'updated_at',)
    search_fields = ('subject', 'review',)
    list_per_page = 20


@admin.register(ReportReview)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'ip',)
    list_filter = ('user', 'review', 'created_at', 'updated_at',)
    search_fields = ('user', 'review',)
    list_per_page = 20
