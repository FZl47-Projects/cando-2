from django.urls import path
from . import views


app_name = 'apps.navigation'

urlpatterns = [
    path('add/', views.CreateAddressView.as_view(), name='create_address'),
    path('delete/', views.DeleteAddressView.as_view(), name='delete_address'),
]
