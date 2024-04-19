from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from apps.core.mixins.views import FilterSimpleListViewMixin, DeleteMixin
from apps.storage import models


class GalleryImageList(FilterSimpleListViewMixin, ListView):
    paginate_by = 15
    template_name = 'dashboard/admin/storage/gallery/list.html'

    def get_queryset(self):
        objects = models.Image.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class GalleryImageDelete(DeleteMixin, View):
    success_message = _('Image Deleted Successfully')

    def get_object(self, request, *args, **kwargs):
        image_id = kwargs.get('image_id')
        return get_object_or_404(models.Image, id=image_id)
