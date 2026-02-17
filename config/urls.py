from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def health_check(request):
    print("DEBUG: Root health check hit!")
    return HttpResponse("OK")

urlpatterns = [
    path('', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/auth/', include('users.urls')),
    path('api/users/', include('users.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/products/', include('products.urls')),
    # Swagger/OpenAPI documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve media files in production manually to ensure they are accessible
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
