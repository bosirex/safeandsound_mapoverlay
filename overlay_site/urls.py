
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('cards/', include('cards.urls')),
    path('', include('cards.urls')),
    path('admin/', admin.site.urls),
    path('overlay/', include('overlay_tool.urls')),
    path('', RedirectView.as_view(url='/overlay/dashboard/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static('/qr_codes/', document_root=(settings.BASE_DIR / 'qr_codes'))
