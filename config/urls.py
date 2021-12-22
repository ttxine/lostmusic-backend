from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from config.yasg import urlpatterns as yasg_urls

urlpatterns = [
    path('lostadmin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('src.music.urls')),
    path('auth/', include('src.oauth.urls')),
    path('auth/', include('src.favorites.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += yasg_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
