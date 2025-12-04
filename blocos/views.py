from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Bloco, Torre, Apartamento
from .forms import BlocoForm, TorreForm, ApartamentoForm

# --- Mixin de Segurança ---
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'eh_admin') and self.request.user.eh_admin

# CENTRAL UNIFICADA DE ESTRUTURA


class GerenciarEstruturaView(AdminRequiredMixin, View):
    template_name = 'blocos/gerenciar_estrutura.html'

    def get(self, request):
        context = {
            'blocos': Bloco.objects.all().order_by('nome'),
            'torres': Torre.objects.select_related('bloco').all().order_by('bloco__nome', 'nome'),
            'apartamentos': Apartamento.objects.select_related('torre__bloco').all().order_by('torre__nome', 'numero'),
            
            'form_bloco': BlocoForm(prefix='bloco'),
            'form_torre': TorreForm(prefix='torre'),
            'form_apto': ApartamentoForm(prefix='apto'),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')

        if action == 'criar_bloco':
            form = BlocoForm(request.POST, prefix='bloco')
            if form.is_valid():
                form.save()
                messages.success(request, "Bloco adicionado!")
            else:
                messages.error(request, "Erro ao criar Bloco.")

        elif action == 'criar_torre':
            form = TorreForm(request.POST, prefix='torre')
            if form.is_valid():
                form.save()
                messages.success(request, "Torre adicionada!")
            else:
                messages.error(request, "Erro ao criar Torre.")

        elif action == 'criar_apto':
            form = ApartamentoForm(request.POST, prefix='apto')
            if form.is_valid():
                form.save()
                messages.success(request, "Apartamento adicionado!")
            else:
                messages.error(request, "Erro ao criar Apartamento.")

        return redirect('gerenciar_estrutura')

# EDIÇÃO E REMOÇÃO (


# --- Blocos ---
class BlocoUpdateView(AdminRequiredMixin, UpdateView):
    model = Bloco
    form_class = BlocoForm
    template_name = 'blocos/bloco_form.html'
    success_url = reverse_lazy('gerenciar_estrutura') 

    def form_valid(self, form):
        messages.success(self.request, "Bloco atualizado.")
        return super().form_valid(form)

class BlocoDeleteView(AdminRequiredMixin, DeleteView):
    model = Bloco
    template_name = 'blocos/confirm_delete.html'
    success_url = reverse_lazy('gerenciar_estrutura') 

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "Bloco removido.")
        return super().delete(request, *args, **kwargs)

# --- Torres ---
class TorreUpdateView(AdminRequiredMixin, UpdateView):
    model = Torre
    form_class = TorreForm
    template_name = 'blocos/torre_form.html'
    success_url = reverse_lazy('gerenciar_estrutura')

    def form_valid(self, form):
        messages.success(self.request, "Torre atualizada.")
        return super().form_valid(form)

class TorreDeleteView(AdminRequiredMixin, DeleteView):
    model = Torre
    template_name = 'blocos/confirm_delete.html'
    success_url = reverse_lazy('gerenciar_estrutura')

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "Torre removida.")
        return super().delete(request, *args, **kwargs)

# --- Apartamentos ---
class ApartamentoUpdateView(AdminRequiredMixin, UpdateView):
    model = Apartamento
    form_class = ApartamentoForm
    template_name = 'blocos/apartamento_form.html'
    success_url = reverse_lazy('gerenciar_estrutura') 

    def form_valid(self, form):
        messages.success(self.request, "Apartamento atualizado.")
        return super().form_valid(form)

class ApartamentoDeleteView(AdminRequiredMixin, DeleteView):
    model = Apartamento
    template_name = 'blocos/confirm_delete.html'
    success_url = reverse_lazy('gerenciar_estrutura') 

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "Apartamento removido.")
        return super().delete(request, *args, **kwargs)