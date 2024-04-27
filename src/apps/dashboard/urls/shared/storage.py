from django.urls import path

from apps.dashboard.views.dashboard.shared import storage as views

urlpatterns = [
    # storage
    path('storage/gallery/list', views.GalleryImageList.as_view(), name='gallery__list'),
    path('storage/gallery/<int:image_id>/delete', views.GalleryImageDelete.as_view(), name='gallery__delete'),
]
