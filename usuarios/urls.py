from django.urls import path
from . import views

urlpatterns = [
    # Rotas de Funcionários
    path('equipe/', views.FuncionarioListView.as_view(), name='funcionario_list'),
    path('equipe/novo/', views.FuncionarioCreateView.as_view(), name='funcionario_create'),
    path('equipe/<int:pk>/editar/', views.FuncionarioUpdateView.as_view(), name='funcionario_update'),
    path('equipe/<int:pk>/remover/', views.FuncionarioDeleteView.as_view(), name='funcionario_delete'),

    # Rotas de Moradores
    path('moradores/', views.MoradorListView.as_view(), name='morador_list'),
    path('moradores/novo/', views.MoradorCreateView.as_view(), name='morador_create'),
    path('moradores/<int:pk>/editar/', views.MoradorUpdateView.as_view(), name='morador_update'),
    path('moradores/<int:pk>/remover/', views.MoradorDeleteView.as_view(), name='morador_delete'),
]