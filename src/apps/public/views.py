from django.shortcuts import render
from django.views.generic import TemplateView


def err_403_handler(request, exception):
    return render(request, 'public/errors/403.html')


def err_404_handler(request, exception):
    return render(request, 'public/errors/404.html')


def err_500_handler(request):
    return render(request, 'public/errors/500.html')


class Index(TemplateView):
    template_name = 'public/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)

        return context
