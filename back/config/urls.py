from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('api/v1/movie/', include('movies.urls')),
    path('api/v1/game/', include('games.urls')),
    path('api/v1/profile/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
