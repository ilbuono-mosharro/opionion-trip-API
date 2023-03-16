from django.urls import path

from . import views

app_name = "cities"

urlpatterns = [
    path('city/<slug:slug>/', views.city_page, name='city_page'),
    path('cities/', views.city_all, name='city_all'),
    path('dashboard/city/status/choice/<uuid:city_id>/', views.staff_city_status, name="staff_city_status"),
    path('dashboard/city/add/', views.add_city, name='add_city'),
    path('dashboard/city/update/<uuid:city_id>/', views.modify_city, name='modify_city'),
    path('dashboard/city/delete/<uuid:city_id>/', views.delete_city, name='delete_city'),
    path('dashboard/city/add/images/<uuid:city_id>/', views.add_image_city, name='add_image_city'),
    path('dashboard/city/delete/image/<uuid:image_id>/image/', views.delete_image_city, name='delete_image_city'),
    path('dashboard/city/update/image/<uuid:image_id>/image/', views.modify_image_city, name='modify_image_city'),
]
