from django.urls import path

from . import views

app_name = "registration"

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-up/info-account-activation/', views.info_account_activation, name='info_account_activation'),
    path('sign-up/confermation-account/<slug:uidb64>/<slug:token>/', views.activate_account, name='activate_account'),
    path('dashboard/accounts/update/profile/', views.update_profile, name='update_profile'),
    path('dashboard/accounts/delete/account/', views.delete_user, name="delete_user"),
]
