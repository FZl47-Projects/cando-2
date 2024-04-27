from django.urls import path

from apps.dashboard.views.dashboard.shared import main as views

urlpatterns = [
    # main
    path('', views.Index.as_view(), name='index'),
]
