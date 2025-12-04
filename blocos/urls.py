from django.urls import path
from . import views

urlpatterns = [
    # Rota Central Unificada
    path('gerenciar/', views.GerenciarEstruturaView.as_view(), name='gerenciar_estrutura'),

    # Rotas de Edição e Remoção (Necessárias para o ID)
    path('blocos/<int:pk>/editar/', views.BlocoUpdateView.as_view(), name='bloco_update'),
    path('blocos/<int:pk>/remover/', views.BlocoDeleteView.as_view(), name='bloco_delete'),

    path('torres/<int:pk>/editar/', views.TorreUpdateView.as_view(), name='torre_update'),
    path('torres/<int:pk>/remover/', views.TorreDeleteView.as_view(), name='torre_delete'),

    path('apartamentos/<int:pk>/editar/', views.ApartamentoUpdateView.as_view(), name='apartamento_update'),
    path('apartamentos/<int:pk>/remover/', views.ApartamentoDeleteView.as_view(), name='apartamento_delete'),
]