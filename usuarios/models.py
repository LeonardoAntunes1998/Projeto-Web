from django.db import models
from django.contrib.auth.models import AbstractUser
from blocos.models import Apartamento

class Funcionario(AbstractUser):
    TIPO_OPERADOR = 'OPERADOR'
    TIPO_ADMIN = 'ADMIN'

    CARGO_CHOICES = [
        (TIPO_OPERADOR, 'Funcionário Operacional'),
        (TIPO_ADMIN, 'Administrador/Síndico'),
    ]
    cargo = models.CharField(
        max_length=20, 
        choices=CARGO_CHOICES, 
        default=TIPO_OPERADOR, 
        verbose_name="Nível de Acesso"
    )
    
    telefone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Funcionário"

    @property
    def eh_admin(self):
        return self.cargo == self.TIPO_ADMIN or self.is_superuser

class Morador(models.Model):
    apto = models.ForeignKey(Apartamento, on_delete=models.PROTECT, related_name="moradores")
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Morador"
        verbose_name_plural = "Moradores"

    def __str__(self):
        return f"{self.nome} ({self.apto})"