from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from apps.core.mixins.views import (UserRoleViewMixin, DeleteViewMixin, CreateViewMixin)
from apps.public import forms, models


class SliderManage(UserRoleViewMixin, CreateViewMixin, ListView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/public/slider/manage.html'
    form = forms.SliderCreateForm
    paginate_by = 20

    def get_queryset(self):
        return models.Slider.objects.all()


class SliderDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    redirect_url = reverse_lazy('dashboard:slider__manage')

    def get_object(self, request, *args, **kwargs):
        slider_id = kwargs.get('slider_id')
        return get_object_or_404(models.Slider, id=slider_id)
