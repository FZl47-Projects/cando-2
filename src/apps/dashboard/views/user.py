from django.views.generic import View, TemplateView, DetailView
from apps.core.auth.mixins import LoginRequiredMixinCustom
from django.shortcuts import HttpResponse


class Index(LoginRequiredMixinCustom, View):

    def get(self, request):
        return HttpResponse('Dashboard')
