from django.apps import AppConfig


class EncomendasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'encomendas'
    def ready(self):
        import encomendas.signals  # <--- Adicione esta linha