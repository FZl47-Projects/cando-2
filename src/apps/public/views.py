from django.shortcuts import render
from django.views.generic import TemplateView

from apps.product import models as product_models


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
        # products
        BasicProduct = product_models.BasicProduct
        context['products__showcase'] = BasicProduct.objects.filter(categories__name='showcase')[:8]
        context['products__best_sellers'] = BasicProduct.objects.get_best_sellers()[:8]
        context['products__news'] = BasicProduct.objects.get_news()[:8]
        context['products__suggested'] = BasicProduct.objects.get_suggested()[:8]
        return context


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
