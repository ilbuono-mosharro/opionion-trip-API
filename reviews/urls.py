from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path('review/create/<slug:slug>/<uuid:pk>/', views.attraction_review, name='attraction_review'),
    path('review/report/<uuid:pk>/', views.report_this_review, name='report_this_review'),
    path('review/vote/<uuid:pk>/', views.add_review_vote, name='add_review_vote'),
    path('dashboard/review/update/<uuid:review_id>/', views.modify_review, name='modify_review'),
    path('dashboard/review/delete/<uuid:review_id>/', views.delete_review, name='delete_review'),
    path('dashboard/review/status/approved/<uuid:review_id>/', views.staff_review_ap, name='staff_review_ap'),
    path('dashboard/review/status/reject/<uuid:review_id>/', views.staff_review_re, name='staff_review_re'),
    path('dashboard/review/status/wating/<uuid:review_id>/', views.staff_review_wa, name='staff_review_wa'),
]
