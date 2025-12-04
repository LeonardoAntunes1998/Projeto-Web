from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Encomenda
from .utils import enviar_notificacao_n8n  # Importamos a função nova

@receiver(post_save, sender=Encomenda)
def notificar_chegada(sender, instance, created, **kwargs):
    if created:
        enviar_notificacao_n8n(instance, tipo="chegada")

@receiver(pre_save, sender=Encomenda)
def verificar_mudanca_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            antiga = Encomenda.objects.get(pk=instance.pk)
            if antiga.status != 'RETIRADA' and instance.status == 'RETIRADA':
                instance._acabou_de_retirar = True
        except Encomenda.DoesNotExist:
            pass

@receiver(post_save, sender=Encomenda)
def notificar_retirada(sender, instance, created, **kwargs):
    if getattr(instance, '_acabou_de_retirar', False):
        enviar_notificacao_n8n(instance, tipo="saida")