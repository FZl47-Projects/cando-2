import abc
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from apps.core.utils import create_form_messages


class BaseCUViewMixin(abc.ABC):
    """
        Base Create & Update View Mixin
    """
    form = None
    success_message = None
    is_success = False
    redirect_url = None

    def do_success(self):
        pass

    def do_fail(self):
        pass

    def get_redirect_url(self):
        if not self.redirect_url:
            self.redirect_url = self.request.META.get('HTTP_REFERER', '/')  # referrer url
        return self.redirect_url

    def set_success_message(self):
        messages.success(self.request, self.success_message)

    def get_data(self, **kwargs):
        data = self.request.POST.copy()
        # add request to data
        data['request'] = self.request
        data.update(**kwargs)
        self.add_additional_data(data)
        return data

    def add_additional_data(self, data, obj=None):
        pass

    def get_form(self):
        return self.form


class CreateViewMixin(BaseCUViewMixin):

    def post(self, request, *args, **kwargs):
        data = self.get_data(**kwargs)
        f = self.get_form()(data=data, files=request.FILES)
        if not f.is_valid():
            # create error message's
            create_form_messages(request, f)
            self.do_fail()
            return redirect(self.get_redirect_url())
        self.obj = f.save()
        self.is_success = True
        self.do_success()
        self.set_success_message()
        return redirect(self.get_redirect_url())


class UpdateViewMixin(BaseCUViewMixin):

    @abc.abstractmethod
    def get_object(self):
        pass

    def post(self, request, *args, **kwargs):
        data = self.get_data()
        obj = self.get_object()
        f = self.get_form()(instance=obj, data=data, files=request.FILES)
        if not f.is_valid():
            # create error message's
            create_form_messages(request, f)
            self.do_fail()
            return redirect(self.get_redirect_url())
        self.obj = f.save()
        self.is_success = True
        self.do_success()
        self.set_success_message()
        return redirect(self.get_redirect_url())


class UpdateMultipleObjViewMixin(BaseCUViewMixin):
    ignore_err = False
    _updated_objects = None

    @abc.abstractmethod
    def get_objects(self):
        pass

    def _to_updated(self, obj):
        if not self._updated_objects:
            self._updated_objects = []
        self._updated_objects.append(obj)

    def get_updated_objects(self):
        return self._updated_objects

    def post(self, request):
        objects = self.get_objects()
        if objects is None:
            raise ValueError(' `get_objects` function must return a sequence(QuerySet or ..) not None type')
        for obj in objects:
            f = self.form(instance=obj, data=request.POST, files=request.FILES)
            if not f.is_valid():
                # create error message's
                create_form_messages(request, f)
                self.do_error()
                if not self.ignore_err:
                    return redirect(self.get_redirect_url())
                continue
            obj = f.save()
            self._to_updated(obj)
        self.do_success()
        self.set_success_message()
        return redirect(self.get_redirect_url())


class FilterSimpleListViewMixin(abc.ABC):
    search_param: str = 'search'
    search_fields: list | tuple = None
    filter_param: str = 'filter'
    filter_fields: list | tuple = None
    filter_param_all: str = 'all'

    def search(self, objects):
        if not self.search_fields:
            return objects
        sp = self.request.GET.get(self.search_param)
        if not sp:
            return objects

        query = Q()
        for field in self.search_fields:
            query |= Q(**{field: sp})
        objects = objects.filter(query)
        return objects

    def filter(self, objects):
        fp = self.request.GET.get(self.filter_param)
        if not fp:
            return objects
        if not self.filter_fields:
            return objects

        filter_fields_kw = {}
        for field in self.filter_fields:
            field_value = self.request.GET.get(field)
            if (not field_value) or (field_value == self.filter_param_all):
                continue
            filter_fields_kw[field] = field_value
        objects = objects.filter(**filter_fields_kw)
        return objects


class DeleteMixin(abc.ABC):
    success_message = None
    is_success = False
    redirect_url = None

    def do_success(self):
        pass

    def do_fail(self):
        pass

    def get_redirect_url(self):
        if not self.redirect_url:
            self.redirect_url = self.request.META.get('HTTP_REFERER', '/')  # referrer url
        return self.redirect_url

    @abc.abstractmethod
    def get_object(self, request, *args, **kwargs):
        pass

    def set_success_message(self):
        messages.success(self.request, self.success_message)

    def dispatch(self, request, *args, **kwargs):
        self.get_object(request, *args, **kwargs).delete()
        self.is_success = True
        self.do_success()
        self.set_success_message()
        return redirect(self.get_redirect_url())
