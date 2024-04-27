from django.urls import path

from apps.dashboard.views.dashboard.shared import account as views

urlpatterns = [
    # user
    path('user/list', views.UserList.as_view(), name='user__list'),
    path('user/<int:user_id>/detail', views.UserDetail.as_view(), name='user__detail'),
    path('user/<int:user_id>/delete', views.UserDelete.as_view(), name='user__delete'),
    path('user/<int:user_id>/update', views.UserUpdate.as_view(), name='user__update'),
]

