from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('apps.public.urls', namespace='public')),
    path('', include('apps.product.urls', namespace='product')),
    path('', include('apps.notification.urls', namespace='notification')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('navigation/', include('apps.navigation.urls', namespace='navigation')),
    path('u/', include('apps.account.urls', namespace='account')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'apps.public.views.err_403_handler'
handler404 = 'apps.public.views.err_404_handler'
handler500 = 'apps.public.views.err_500_handler'
