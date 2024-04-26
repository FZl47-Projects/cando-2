from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import View, ListView, TemplateView

from apps.core.auth import object_access
from apps.core.mixins.views import (
    CreateViewMixin, UserRoleViewMixin,
    MultipleUserListViewMixin, FilterSimpleListViewMixin,
    MultipleUserViewMixin, DeleteViewMixin
)
from apps.notification import forms, models


class NotificationUserCreate(UserRoleViewMixin, CreateViewMixin, View):
    role_access = ('super_user',)
    form = forms.NotificationUserCreateForm
    success_message = _('Notification User Created Successfully')


class NotificationUserList(UserRoleViewMixin, FilterSimpleListViewMixin, ListView):
    role_access = ('super_user',)
    paginate_by = 20
    search_fields = ('title__icontains',)
    template_name = 'dashboard/admin/notification/list.html'

    def get_queryset(self):
        objects = models.NotificationUser.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class NotificationPersonalList(MultipleUserListViewMixin, FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('title__icontains',)
    super_user_template = 'dashboard/admin/notification/personal-list.html'
    user_template = 'dashboard/user/notification/personal-list.html'

    def get_queryset(self):
        objects = self.request.user.get_notifications()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class NotificationDetail(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/notification/detail.html'
    user_template = 'dashboard/user/notification/detail.html'

    def get_context_data(self, **kwargs):
        notification_id = kwargs.get('notification_id')
        notification = get_object_or_404(models.NotificationUser, id=notification_id)
        object_access(notification, self.request.user, user_field='to_user')
        if notification.seen is False:
            if self.request.user == notification.to_user:
                notification.seen = True
                notification.save()
        context = {
            'notification': notification
        }
        return context


class NotificationDelete(DeleteViewMixin, View):
    success_message = _('Operation Successfully Completed')

    def get_object(self, request, *args, **kwargs):
        notification_id = kwargs.get('notification_id')
        notification = get_object_or_404(models.NotificationUser, id=notification_id)
        object_access(notification, self.request.user, user_field='to_user')
        return notification

    def get_redirect_url(self):
        user_role = self.request.user.role
        if user_role == 'super_user':
            return reverse('dashboard:notification_user__list')
        return reverse('dashboard:notification_user_personal__list')
