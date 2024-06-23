from .models import BasicProduct


def deactivation_of_showcase_products():
    BasicProduct.objects.filter(type='showcase', status='active').update(status='inactive')
