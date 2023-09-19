from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from shop.views import CustomAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('shop.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/token-auth/', CustomAuthToken.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
