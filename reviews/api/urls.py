from django.urls import path

from . import views

urlpatterns = [
    path('reviews/', views.ReviewRatingList.as_view(), name="reviews"),
    path('reviews/<uuid:pk>/', views.ReviewRatingDetail.as_view(), name="reviews_rud"),
    path('reviews/<uuid:pk>/add-or-remove-vote/', views.AddOrRemoveVote.as_view(), name="manage_vote"),
    path('report-review/<uuid:pk>/', views.ReportReviewCreate.as_view(), name="report-review"),
]
