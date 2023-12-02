from django.shortcuts import render
from django.views import View
from apps.core.auth.mixins import LoginRequiredMixinCustom


class Index(LoginRequiredMixinCustom, View):
    pass
