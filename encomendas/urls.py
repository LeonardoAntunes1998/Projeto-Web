from django.urls import path
from . import views

urlpatterns = [
    # Dashboard e Operação
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('nova/', views.EncomendaCreateView.as_view(), name='encomenda_create'),
    path('<int:pk>/', views.EncomendaDetailView.as_view(), name='encomenda_detail'),
    path('<int:pk>/retirar/', views.ConfirmarRetiradaView.as_view(), name='confirmar_retirada'),
    
    # API Ajax
    path('ajax/carregar-dados/', views.carregar_dados_locais, name='ajax_carregar_dados'),

    # Gestão de Transportadoras (Admin)
    path('transportadoras/', views.TransportadoraListView.as_view(), name='transportadora_list'),
    path('transportadoras/nova/', views.TransportadoraCreateView.as_view(), name='transportadora_create'),
    path('transportadoras/<int:pk>/editar/', views.TransportadoraUpdateView.as_view(), name='transportadora_update'),
    path('transportadoras/<int:pk>/remover/', views.TransportadoraDeleteView.as_view(), name='transportadora_delete'),
    
    # URLs de automação e notificações 
    path('encomenda/<int:pk>/lembrar/', views.enviar_lembrete, name='enviar_lembrete'),
    path('encomenda/<int:pk>/reenviar-codigo/', views.reenviar_codigo, name='reenviar_codigo'),

]