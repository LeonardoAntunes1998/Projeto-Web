from django import forms
from .models import Encomenda, Transportadora

class EncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = ['morador', 'transportadora', 'codigo_encomenda', 'descricao', 'foto']
        widgets = {
            'morador': forms.Select(attrs={'class': 'form-select'}),
            'transportadora': forms.Select(attrs={'class': 'form-select'}),
            'codigo_encomenda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Rastreio ou ID'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descrição do pacote'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

class TransportadoraForm(forms.ModelForm):
    class Meta:
        model = Transportadora
     
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: DHL, Loggi, Correios'}),
        }