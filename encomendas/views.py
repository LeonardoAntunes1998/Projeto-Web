from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse

from .models import Encomenda, LogMovimentacao, Transportadora
from .forms import EncomendaForm, TransportadoraForm
from blocos.models import Bloco, Torre, Apartamento
from usuarios.models import Morador

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Encomenda
from .utils import enviar_notificacao_n8n # Importamos a mesma função


# OPERAÇÃO DIÁRIA (DASHBOARD, ENCOMENDAS, BAIXA)

class DashboardView(LoginRequiredMixin, ListView):
    model = Encomenda
    template_name = 'encomendas/dashboard.html'
    context_object_name = 'encomendas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Encomenda.objects.filter(ativo=True).select_related(
            'morador', 
            'morador__apto', 
            'morador__apto__torre', 
            'morador__apto__torre__bloco'
        ).order_by('status', '-data_entrada')

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(codigo_encomenda__icontains=q) | 
                Q(morador__nome__icontains=q) |
                Q(morador__apto__numero__icontains=q)
            )

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        bloco_id = self.request.GET.get('bloco')
        if bloco_id:
            queryset = queryset.filter(morador__apto__torre__bloco_id=bloco_id)

        torre_id = self.request.GET.get('torre')
        if torre_id:
            queryset = queryset.filter(morador__apto__torre_id=torre_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['total_pendentes'] = Encomenda.objects.filter(status='PENDENTE', ativo=True).count()
        context['total_retiradas'] = Encomenda.objects.filter(status='RETIRADA', ativo=True).count()
        
        context['blocos'] = Bloco.objects.all().order_by('nome')
        
        context['filtro_q'] = self.request.GET.get('q', '')
        context['filtro_status'] = self.request.GET.get('status', '')
        context['filtro_bloco'] = self.request.GET.get('bloco', '')
        context['filtro_torre'] = self.request.GET.get('torre', '')
        
        if context['filtro_bloco']:
            context['torres_filtradas'] = Torre.objects.filter(bloco_id=context['filtro_bloco']).order_by('nome')
            
        return context

class EncomendaCreateView(LoginRequiredMixin, CreateView):
    model = Encomenda
    form_class = EncomendaForm
    template_name = 'encomendas/encomenda_form.html'
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        initial = super().get_initial()
        # Se vier morador na URL (modo repetição), já preenche o form
        morador_id = self.request.GET.get('morador_id')
        if morador_id:
            initial['morador'] = morador_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blocos'] = Bloco.objects.all().order_by('nome')
        
 
        morador_id = self.request.GET.get('morador_id')
        if morador_id:
            morador = get_object_or_404(Morador, pk=morador_id)
            bloco_atual = morador.apto.torre.bloco
            torre_atual = morador.apto.torre
            
            context['bloco_atual_id'] = bloco_atual.id
            context['torre_atual_id'] = torre_atual.id
            context['apto_atual_id'] = morador.apto.id
            
            context['torres_atuais'] = Torre.objects.filter(bloco=bloco_atual).order_by('nome')
            context['aptos_atuais'] = Apartamento.objects.filter(torre=torre_atual).order_by('numero')
            
            # Avisa o template que estamos em modo de repetição
            context['modo_repeticao'] = True
            context['morador_nome'] = morador.nome
            
        return context

    def form_valid(self, form):
        form.instance.funcionario_registro = self.request.user
        self.object = form.save()
        
        LogMovimentacao.objects.create(
            encomenda=self.object,
            funcionario=self.request.user,
            acao='REGISTRO',
            detalhes=f"Registrado para {self.object.morador}"
        )
        
        # Verifica qual botão foi clicado
        if 'save_add_another' in self.request.POST:
            messages.success(self.request, f"Encomenda salva! Adicione a próxima para {self.object.morador.nome}.")
            # Redireciona para a mesma página com o ID do morador na URL
            url = reverse('encomenda_create') + f"?morador_id={self.object.morador.id}"
            return redirect(url)
        
        messages.success(self.request, "Encomenda registrada com sucesso.")
        return redirect(self.success_url)

class EncomendaDetailView(LoginRequiredMixin, DetailView):
    model = Encomenda
    template_name = 'encomendas/encomenda_detail.html'
    context_object_name = 'encomenda'

class ConfirmarRetiradaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        encomenda = get_object_or_404(Encomenda, pk=pk)
        
        if encomenda.status == 'RETIRADA':
            messages.warning(request, "Esta encomenda já foi retirada.")
            return redirect('encomenda_detail', pk=pk)
            
        codigo_input = request.POST.get('codigo_input')
        
        if not codigo_input or codigo_input.strip().upper() != encomenda.codigo_retirada:
            messages.error(request, "Código incorreto! A entrega não foi autorizada.")
            return redirect('encomenda_detail', pk=pk)
            
        encomenda.status = 'RETIRADA'
        encomenda.data_retirada = timezone.now()
        encomenda.save()
        
        LogMovimentacao.objects.create(
            encomenda=encomenda,
            funcionario=request.user,
            acao='RETIRADA',
            detalhes=f"Baixa via código: {encomenda.codigo_retirada}"
        )
        messages.success(request, "Código validado! Encomenda entregue com sucesso.")
        return redirect('dashboard')

def carregar_dados_locais(request):
    tipo = request.GET.get('tipo')
    pai_id = request.GET.get('id')
    dados = []

    if tipo == 'torres' and pai_id:
        objetos = Torre.objects.filter(bloco_id=pai_id).order_by('nome')
        for obj in objetos:
            dados.append({'id': obj.id, 'nome': obj.nome})
            
    elif tipo == 'apartamentos' and pai_id:
        objetos = Apartamento.objects.filter(torre_id=pai_id).order_by('numero')
        for obj in objetos:
            dados.append({'id': obj.id, 'nome': obj.numero})
            
    elif tipo == 'moradores' and pai_id:
        objetos = Morador.objects.filter(apto_id=pai_id).order_by('nome')
        for obj in objetos:
            dados.append({'id': obj.id, 'nome': obj.nome})

    return JsonResponse(dados, safe=False)


# GESTÃO DE TRANSPORTADORAS (OPERADOR + ADMIN)


class TransportadoraListView(LoginRequiredMixin, ListView):
    model = Transportadora
    template_name = 'encomendas/transportadora_list.html'
    context_object_name = 'transportadoras'
    ordering = ['nome']

class TransportadoraCreateView(LoginRequiredMixin, CreateView):
    model = Transportadora
    form_class = TransportadoraForm
    template_name = 'encomendas/transportadora_form.html'
    success_url = reverse_lazy('transportadora_list')

    def form_valid(self, form):
        messages.success(self.request, "Transportadora cadastrada com sucesso.")
        return super().form_valid(form)

class TransportadoraUpdateView(LoginRequiredMixin, UpdateView):
    model = Transportadora
    form_class = TransportadoraForm
    template_name = 'encomendas/transportadora_form.html'
    success_url = reverse_lazy('transportadora_list')

    def form_valid(self, form):
        messages.success(self.request, "Transportadora atualizada.")
        return super().form_valid(form)

class TransportadoraDeleteView(LoginRequiredMixin, DeleteView):
    model = Transportadora
    template_name = 'encomendas/transportadora_confirm_delete.html'
    success_url = reverse_lazy('transportadora_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "Transportadora removida.")
        return super().delete(request, *args, **kwargs)
    
    # Função para enviar automação via N8N

def enviar_lembrete(request, pk):
    # 1. Pega a encomenda pelo ID (pk)
    encomenda = get_object_or_404(Encomenda, pk=pk)
    
    # 2. Chama a função de envio com o tipo 'lembrete'
    sucesso = enviar_notificacao_n8n(encomenda, tipo="lembrete")
    
    # 3. Avisa o porteiro na tela se deu certo ou não
    if sucesso:
        messages.success(request, f"Lembrete enviado para {encomenda.morador}!")
    else:
        messages.error(request, "Erro ao enviar. Verifique o telefone do morador.")
    
    # 4. Volta para a tela de detalhes
    return redirect('encomenda_detail', pk=pk)
# ... (imports e função enviar_lembrete) ...

def reenviar_codigo(request, pk):
    # 1. Pega a encomenda
    encomenda = get_object_or_404(Encomenda, pk=pk)
    
    # 2. Chama o utils com o tipo NOVO
    sucesso = enviar_notificacao_n8n(encomenda, tipo="reenvio_codigo")
    
    # 3. Avisa na tela
    if sucesso:
        messages.success(request, f"Código reenviado com sucesso para {encomenda.morador}!")
    else:
        messages.error(request, "Erro ao reenviar código. Verifique o telefone.")
    
    # 4. Recarrega a página
    return redirect('encomenda_detail', pk=pk)