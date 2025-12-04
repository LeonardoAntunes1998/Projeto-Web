from django.urls import path
from . import views

urlpatterns = [
    path('estatisticas/', views.EstatisticasView.as_view(), name='relatorio_estatisticas'),
    path('auditoria/', views.AuditoriaView.as_view(), name='relatorio_auditoria'),
    path('exportar/csv/', views.ExportarCSVView.as_view(), name='relatorio_exportar_csv'),
    path('exportar/pdf/', views.ExportarPDFView.as_view(), name='relatorio_exportar_pdf'),
]