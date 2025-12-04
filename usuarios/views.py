from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import Funcionario, Morador
from .forms import FuncionarioForm, MoradorForm
from blocos.models import Bloco, Torre, Apartamento

# Mixin de Permissão (Apenas Admin)
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.eh_admin

# --- Views de Funcionários (Restritas ao Admin) ---

class FuncionarioListView(AdminRequiredMixin, ListView):
    model = Funcionario
    template_name = 'usuarios/funcionario_list.html'
    context_object_name = 'funcionarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = Funcionario.objects.all().order_by('username')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(username__icontains=q) | 
                Q(first_name__icontains=q)
            )
        return queryset

class FuncionarioCreateView(AdminRequiredMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'usuarios/funcionario_form.html'
    success_url = reverse_lazy('funcionario_list')

    def form_valid(self, form):
        messages.success(self.request, "Funcionário cadastrado com sucesso!")
        return super().form_valid(form)

class FuncionarioUpdateView(AdminRequiredMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'usuarios/funcionario_form.html'
    success_url = reverse_lazy('funcionario_list')

    def form_valid(self, form):
        messages.success(self.request, "Dados do funcionário atualizados.")
        return super().form_valid(form)

class FuncionarioDeleteView(AdminRequiredMixin, DeleteView):
    model = Funcionario
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('funcionario_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "Funcionário removido com sucesso.")
        return super().delete(request, *args, **kwargs)


# --- Views de Moradores (Acesso Liberado para Operadores e Admins) ---

class MoradorListView(LoginRequiredMixin, ListView):
    model = Morador
    template_name = 'usuarios/morador_list.html'
    context_object_name = 'moradores'
    paginate_by = 20

    def get_queryset(self):
        queryset = Morador.objects.select_related('apto__torre__bloco').all().order_by('nome')
        
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(nome__icontains=q)
        
        bloco_id = self.request.GET.get('bloco')
        torre_id = self.request.GET.get('torre')
        apto_id = self.request.GET.get('apto')

        if bloco_id:
            queryset = queryset.filter(apto__torre__bloco_id=bloco_id)
        if torre_id:
            queryset = queryset.filter(apto__torre_id=torre_id)
        if apto_id:
            queryset = queryset.filter(apto_id=apto_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['blocos'] = Bloco.objects.all().order_by('nome')
        
        filtro_bloco = self.request.GET.get('bloco', '')
        filtro_torre = self.request.GET.get('torre', '')
        filtro_apto = self.request.GET.get('apto', '')
        
        context['filtro_bloco'] = filtro_bloco
        context['filtro_torre'] = filtro_torre
        context['filtro_apto'] = filtro_apto
        context['filtro_q'] = self.request.GET.get('q', '')

        if filtro_bloco:
            context['torres_filtradas'] = Torre.objects.filter(bloco_id=filtro_bloco).order_by('nome')
        if filtro_torre:
            context['aptos_filtrados'] = Apartamento.objects.filter(torre_id=filtro_torre).order_by('numero')

        return context

class MoradorCreateView(LoginRequiredMixin, CreateView):
    model = Morador
    form_class = MoradorForm
    template_name = 'usuarios/morador_form.html'
    success_url = reverse_lazy('morador_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blocos'] = Bloco.objects.all().order_by('nome')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Morador cadastrado com sucesso!")
        return super().form_valid(form)

class MoradorUpdateView(LoginRequiredMixin, UpdateView):
    model = Morador
    form_class = MoradorForm
    template_name = 'usuarios/morador_form.html'
    success_url = reverse_lazy('morador_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blocos'] = Bloco.objects.all().order_by('nome')
        
        morador = self.object
        if morador.apto:
            bloco_atual = morador.apto.torre.bloco
            torre_atual = morador.apto.torre
            
            context['bloco_atual_id'] = bloco_atual.id
            context['torre_atual_id'] = torre_atual.id
            context['apto_atual_id'] = morador.apto.id
            
            context['torres_atuais'] = Torre.objects.filter(bloco=bloco_atual).order_by('nome')
            context['aptos_atuais'] = Apartamento.objects.filter(torre=torre_atual).order_by('numero')
            
        return context

    def form_valid(self, form):
        messages.success(self.request, "Dados do morador atualizados.")
        return super().form_valid(form)

class MoradorDeleteView(LoginRequiredMixin, DeleteView):
    model = Morador
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('morador_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "Morador removido.")
        return super().delete(request, *args, **kwargs)