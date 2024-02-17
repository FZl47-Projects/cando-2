from django.urls import path
from . import views


app_name = 'apps.public'

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
]
