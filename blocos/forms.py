from django import forms
from .models import Bloco, Torre, Apartamento

class BlocoForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Bloco A, Setor Norte'}),
        }

class TorreForm(forms.ModelForm):
    class Meta:
        model = Torre
        fields = ['bloco', 'nome']
        widgets = {
            'bloco': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Torre 1, Edifício Hibisco'}),
        }

class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        fields = ['torre', 'numero']
        widgets = {
            'torre': forms.Select(attrs={'class': 'form-select'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 101, 1204B'}),
        }