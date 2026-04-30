from django.contrib import admin
from django.urls import path, include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('admin/admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    # Schema faylini generatsiya qilish (JSON formatida)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI: Interaktiv dokumentatsiya
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Redoc: Muqobil va chiroyli dizayndagi dokumentatsiya
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
