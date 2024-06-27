from apps.core.utils import add_urls_module
from . import (main, product, payment, storage, notifications, account, navigation, public)

app_name = 'apps.dashboard'
urlpatterns = []
add_urls_module(urlpatterns, main, product, payment, storage, storage, notifications, account, navigation, public)
