from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# urlpatterns = [
#     # YOUR PATTERNS
#     # Optional UI:
# ]

urlpatterns = [
    # docs 
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),        
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('admin/', admin.site.urls),
    path('api/v1/'  , 
        include(
            [
                path('', include('app.store.urls')),

            ]
        ))
]
