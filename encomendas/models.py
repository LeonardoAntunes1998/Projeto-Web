import random
import string
from django.db import models
from django.utils.timezone import now 
from usuarios.models import Morador, Funcionario

def generate_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

class Transportadora(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome")
    
    codigo = models.SlugField(
        max_length=50, 
        unique=True, 
        editable=False, 
        null=True,
        blank=True,
        verbose_name="Código Identificador"
    )

    class Meta:
        verbose_name = "Transportadora"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Encomenda(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('RETIRADA', 'Retirada'),
    ]

    morador = models.ForeignKey(Morador, on_delete=models.PROTECT, related_name='encomendas')
    
    funcionario_registro = models.ForeignKey(
        Funcionario, 
        on_delete=models.PROTECT, 
        related_name='encomendas_registradas', 
        verbose_name="Registrado por"
    )
    
    transportadora = models.ForeignKey(
        Transportadora,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    codigo_encomenda = models.CharField(max_length=30, verbose_name="Código de Rastreio")
    
    codigo_retirada = models.CharField(
        max_length=6,
        default=generate_code,
        unique=True,
        editable=False,
        verbose_name="Código de Retirada"
    )

    descricao = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descrição Visual")

    foto = models.ImageField(
        upload_to="encomendas_fotos/",
        blank=True,
        null=True,
        verbose_name="Foto/Comprovante"
    )

    data_entrada = models.DateTimeField(auto_now_add=True)
    data_retirada = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    
    ativo = models.BooleanField(default=True, verbose_name="Ativo (Deleção Lógica)")

    #relação de dias parados encoemndas
    @property
    def dias_em_espera(self):
        """Retorna quantos dias a encomenda está parada (se pendente)."""
        if self.status == 'PENDENTE' and self.data_entrada:
            delta = now() - self.data_entrada
            return delta.days
        return 0

    @property
    def status_prazo(self):
        """Define a classe de alerta baseada no tempo de espera."""
        dias = self.dias_em_espera
        if dias >= 7:
            return 'CRITICO' # Vermelho
        elif dias >= 3:
            return 'ATENCAO' # Amarelo
        return 'NORMAL'

    def save(self, *args, **kwargs):
        if not self.codigo_retirada:
            self.codigo_retirada = generate_code()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Encomenda"
        verbose_name_plural = "Encomendas"

    def __str__(self):
        return f"#{self.codigo_encomenda} - {self.morador.nome}"

class LogMovimentacao(models.Model):
    ACAO_CHOICES = [
        ('REGISTRO', 'Registro de Entrada'),
        ('RETIRADA', 'Baixa de Retirada'),
        ('EDICAO', 'Edição de Dados'),
        ('DELECAO_ADM', 'Deleção Lógica'),
    ]

    encomenda = models.ForeignKey(Encomenda, on_delete=models.CASCADE, related_name='logs')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT)
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    detalhes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Log de Movimentação"

    def __str__(self):
        return f"{self.acao} - {self.encomenda}"