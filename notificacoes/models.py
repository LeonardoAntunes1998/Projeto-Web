from django.db import models
from usuarios.models import Morador

class Notificacao(models.Model):
    morador = models.ForeignKey(Morador, on_delete=models.CASCADE)
    mensagem = models.TextField()
    enviada_em = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"Msg para {self.morador.nome} em {self.enviada_em}"