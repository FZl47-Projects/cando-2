from django.shortcuts import render, HttpResponse
from django.views import View
from apps.core.auth.mixins import LoginRequiredMixinCustom


class Index(LoginRequiredMixinCustom, View):

    def get(self,request):
        return HttpResponse('Dashboard')
