from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.core.settings import get_default_address
from apps.product import models as product_models
from apps.public import models


def err_403_handler(request, exception):
    return render(request, 'public/errors/403.html')


def err_404_handler(request, exception):
    return render(request, 'public/errors/404.html')


def err_500_handler(request):
    return render(request, 'public/errors/500.html')


class Index(TemplateView):
    template_name = 'public/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products__showcase'] = product_models.BasicProduct.objects.get_showcases()
        context['sliders'] = models.Slider.objects.all()
        return context


class SuccessView(TemplateView):
    template_name = 'public/success_page.html'


class FailView(TemplateView):
    template_name = 'public/fail_page.html'


class Cart(TemplateView):
    template_name = 'public/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart = user.get_current_cart_or_create()
        else:
            cart = product_models.Cart.get_session_cart(self.request)
        context['cart'] = cart
        return context


class CartCheckout(LoginRequiredMixin, View):
    template_name = 'public/checkout.html'

    def get(self, request):
        context = {}
        user = self.request.user
        cart = user.get_current_cart_or_create()
        if cart.has_empty():
            return redirect('public:cart')
        context['cart'] = cart
        context['addresses'] = user.get_addresses() | get_default_address()
        # delivery time
        delivery_time = self.request.GET.get('delivery_time')
        if not delivery_time:
            return redirect('public:cart')
        context['delivery_time'] = delivery_time
        cart.delivery_time = delivery_time
        return render(request, self.template_name, context)
