import csv
from datetime import timedelta
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q, Value
from django.db.models.functions import TruncDate, Concat
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from encomendas.models import Encomenda, LogMovimentacao

# Mixin de permissão (apenas Admin)
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'eh_admin') and self.request.user.eh_admin

# =============================================================================
# DASHBOARD ESTATÍSTICO
# =============================================================================

class EstatisticasView(LoginRequiredMixin, TemplateView):
    template_name = 'relatorios/estatisticas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtros da URL
        dias = int(self.request.GET.get('dias', 30))
        agrupamento = self.request.GET.get('agrupamento', 'bloco') # bloco, torre, apto
        status_local = self.request.GET.get('status_local', 'todos') # todos, PENDENTE, RETIRADA
        
        data_limite = timezone.now() - timedelta(days=dias)
        
        # Querysets Base
        qs_total = Encomenda.objects.filter(ativo=True)
        qs_periodo = qs_total.filter(data_entrada__gte=data_limite)
        
        # KPIs Gerais
        context['total_entradas'] = qs_periodo.count()
        context['total_saidas'] = qs_total.filter(data_retirada__gte=data_limite).count()
        context['estoque_atual'] = qs_total.filter(status='PENDENTE').count()
        
        # Passa filtros de volta para o template
        context['dias_filtro'] = dias
        context['agrupamento_atual'] = agrupamento
        context['status_local_atual'] = status_local

        # 1. Gráfico de Fluxo (Comparativo Diário)
        lista_datas = [timezone.now().date() - timedelta(days=x) for x in range(dias, -1, -1)]
        lista_datas_str = [d.strftime('%d/%m') for d in lista_datas]

        entradas_bd = qs_periodo.annotate(data=TruncDate('data_entrada')).values('data').annotate(qtd=Count('id'))
        saidas_bd = qs_total.filter(data_retirada__gte=data_limite).annotate(data=TruncDate('data_retirada')).values('data').annotate(qtd=Count('id'))

        dict_entradas = {item['data']: item['qtd'] for item in entradas_bd}
        dict_saidas = {item['data']: item['qtd'] for item in saidas_bd}

        context['chart_datas'] = lista_datas_str
        context['chart_entrada'] = [dict_entradas.get(d, 0) for d in lista_datas]
        context['chart_saida'] = [dict_saidas.get(d, 0) for d in lista_datas]

        # 2. Gráfico de Volume por Estrutura (Dinâmico e Filtrável)
        
        # Aplica filtro de status primeiro para este gráfico específico
        qs_estrutura = qs_periodo
        if status_local != 'todos':
            qs_estrutura = qs_estrutura.filter(status=status_local)

        # Define o agrupamento e o campo de label
        if agrupamento == 'apto':
            # CORREÇÃO: Concatena "Numero - Torre" para diferenciar 101A de 101B
            qs_estrutura = qs_estrutura.annotate(
                label_apto=Concat(
                    'morador__apto__numero', 
                    Value(' - '), 
                    'morador__apto__torre__nome'
                )
            )
            campo_group = 'label_apto'
        elif agrupamento == 'torre':
            campo_group = 'morador__apto__torre__nome'
        else:
            # Padrão: Bloco
            campo_group = 'morador__apto__torre__bloco__nome'

        # Agrega e Ordena (Top 10)
        por_estrutura = qs_estrutura.values(campo_group).annotate(total=Count('id')).order_by('-total')[:10]
        
        context['est_labels'] = [e[campo_group] for e in por_estrutura]
        context['est_data'] = [e['total'] for e in por_estrutura]

        # 3. Gráfico de Transportadoras (Top 4 + Outros)
        raw_transp = qs_periodo.values('transportadora__nome').annotate(total=Count('id')).order_by('-total')
        
        top_limit = 4
        top_transp = list(raw_transp[:top_limit])
        resto_transp = raw_transp[top_limit:]

        if resto_transp:
            total_outros = sum(item['total'] for item in resto_transp)
            top_transp.append({'transportadora__nome': 'Outros', 'total': total_outros})

        context['transp_labels'] = [item['transportadora__nome'] if item['transportadora__nome'] else 'Não Inf.' for item in top_transp]
        context['transp_data'] = [item['total'] for item in top_transp]

        return context

# =============================================================================
# LOG DE AUDITORIA
# =============================================================================

class AuditoriaView(AdminRequiredMixin, ListView):
    model = LogMovimentacao
    template_name = 'relatorios/auditoria.html'
    context_object_name = 'logs'
    paginate_by = 50

    def get_queryset(self):
        qs = LogMovimentacao.objects.select_related('encomenda', 'funcionario', 'encomenda__morador').all().order_by('-timestamp')
        
        q = self.request.GET.get('q')
        funcionario = self.request.GET.get('funcionario')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            qs = qs.filter(
                Q(encomenda__codigo_encomenda__icontains=q) |
                Q(encomenda__morador__nome__icontains=q) |
                Q(detalhes__icontains=q)
            )
        if funcionario:
            qs = qs.filter(funcionario__username__icontains=funcionario)
        if data_inicio:
            qs = qs.filter(timestamp__date__gte=data_inicio)
        if data_fim:
            qs = qs.filter(timestamp__date__lte=data_fim)

        return qs

# =============================================================================
# EXPORTAÇÃO DE DADOS
# =============================================================================

class ExportarCSVView(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_entregas.csv"'

        writer = csv.writer(response)
        writer.writerow(['Codigo', 'Morador', 'Apto', 'Bloco', 'Data Entrada', 'Data Saida', 'Status', 'Transportadora'])

        data_limite = timezone.now() - timedelta(days=90)
        encomendas = Encomenda.objects.filter(data_entrada__gte=data_limite).select_related(
            'morador', 'morador__apto', 'transportadora'
        )

        for enc in encomendas:
            writer.writerow([
                enc.codigo_encomenda,
                enc.morador.nome,
                enc.morador.apto.numero,
                enc.morador.apto.torre.bloco.nome,
                enc.data_entrada.strftime('%d/%m/%Y %H:%M'),
                enc.data_retirada.strftime('%d/%m/%Y %H:%M') if enc.data_retirada else '-',
                enc.get_status_display(),
                enc.transportadora.nome if enc.transportadora else '-'
            ])
        return response

class ExportarPDFView(LoginRequiredMixin, View):
    def get(self, request):
        dias = int(request.GET.get('dias', 30))
        data_limite = timezone.now() - timedelta(days=dias)
        
        qs_total = Encomenda.objects.filter(ativo=True)
        qs_periodo = qs_total.filter(data_entrada__gte=data_limite).select_related('morador', 'morador__apto', 'transportadora').order_by('-data_entrada')

        kpis = {
            'entradas': qs_periodo.count(),
            'saidas': qs_total.filter(data_retirada__gte=data_limite).count(),
            'estoque': qs_total.filter(status='PENDENTE').count()
        }

        top_blocos = qs_periodo.values('morador__apto__torre__bloco__nome')\
            .annotate(total=Count('id'))\
            .order_by('-total')[:5]

        top_transp = qs_periodo.values('transportadora__nome')\
            .annotate(total=Count('id'))\
            .order_by('-total')[:5]

        context = {
            'encomendas': qs_periodo,
            'data_geracao': timezone.now(),
            'dias_filtro': dias,
            'kpis': kpis,
            'top_blocos': top_blocos,
            'top_transp': top_transp,
        }
        
        template_path = 'relatorios/pdf_template.html'
        template = get_template(template_path)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="relatorio_gobox_{dias}dias.pdf"'
        
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)
        return response