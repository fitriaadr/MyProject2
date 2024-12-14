from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # URL untuk aplikasi 'users'
    path('vegetables_prices/', include('vegetables_prices.urls')),  # URL untuk aplikasi 'vegetables_prices'
]

# Hanya tambahkan ini saat DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
