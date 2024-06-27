from django.urls import path

from apps.dashboard.views.dashboard.shared import public as views

urlpatterns = [
    # slider
    path('slider/manage', views.SliderManage.as_view(), name='slider__manage'),
    path('slider/<int:slider_id>/delete', views.SliderDelete.as_view(), name='slider__delete'),
]
