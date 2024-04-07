from django.views.generic import TemplateView
from apps.product.models import Cart, WishList


class HeaderComponentView(TemplateView):
    template_name = 'base/components/header.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # get cart and wishlist
        if user.is_authenticated:
            cart = user.get_current_cart_or_create()
            wishlist = user.get_or_create_wishlist()
        else:
            cart = Cart.get_session_cart(self.request)
            wishlist = WishList.get_session_wishlist(self.request)
        context.update({
            'cart': cart,
            'wishlist': wishlist
        })
        return context
