from django.urls import path

from apps.dashboard.views.dashboard.shared import notification as views

urlpatterns = [
    path('notification-user/create', views.NotificationUserCreate.as_view(),
         name='notification_user__create'),
    path('notification-user/list', views.NotificationUserList.as_view(),
         name='notification_user__list'),
    path('notification-user/personal/list', views.NotificationPersonalList.as_view(),
         name='notification_user_personal__list'),

    path('notification-user/<int:notification_id>/detail', views.NotificationDetail.as_view(),
         name='notification_user__detail'),

    path('notification-user/<int:notification_id>/delete', views.NotificationDelete.as_view(),
         name='notification_user__delete'),
]
