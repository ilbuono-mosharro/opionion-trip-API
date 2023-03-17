from django.urls import path

from . import views

app_name = "places"

urlpatterns = [
    path('attractions/', views.attraction_all, name='attraction_all'),
    path('attraction/<slug:slug>/', views.attraction_page, name='attraction_page'),
    path('dashboard/attraction/add/', views.add_attraction, name='add_attraction'),
    path('dashboard/attraction/update/<uuid:attraction_id>/', views.modify_attraction, name='modify_attraction'),
    path('dashboard/attraction/delete/<uuid:attraction_id>/', views.delete_attraction, name='delete_attraction'),
    path('dashboard/attraction/add/wishlist/', views.attraction_wishlist, name='attraction_wishlist'),
    path('dashboard/attraction/status/<uuid:attraction_id>/', views.staff_attraction_status, name='staff_attraction_status'),
    path('dashboard/attraction/add/image/<uuid:attraction_id>/', views.add_image_attraction, name='add_image_attraction'),
    path('dashboard/attraction/delete/image/<uuid:image_id>/', views.delete_image_attraction, name='delete_image_attraction'),
    path('dashboard/attraction/modify/image/<uuid:image_id>/', views.modify_image_attraction, name='modify_image_attraction'),
]
