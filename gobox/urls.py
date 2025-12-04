from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Rotas de Gestão
    path('gestao/', include('usuarios.urls')),
    path('unidades/', include('blocos.urls')), # NOVA LINHA
    path('relatorios/', include('relatorios.urls')),

    # Rotas Principais
    path('', include('encomendas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)