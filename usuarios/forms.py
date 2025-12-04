from django import forms
from .models import Funcionario, Morador

class FuncionarioForm(forms.ModelForm):
  
    password = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Preencha apenas se for criar um novo usuário ou alterar a senha atual."
    )

    class Meta:
        model = Funcionario
        fields = ['username', 'first_name', 'last_name', 'email', 'cargo', 'telefone', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
 
        if password:
            user.set_password(password)
        
        # Define permissões de sistema baseadas no cargo
        if user.cargo == Funcionario.TIPO_ADMIN:
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
            
        if commit:
            user.save()
        return user


class MoradorForm(forms.ModelForm):
    class Meta:
        model = Morador
        fields = ['nome', 'apto', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'apto': forms.Select(attrs={'class': 'form-select'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) 9XXXX-XXXX'}),
        }