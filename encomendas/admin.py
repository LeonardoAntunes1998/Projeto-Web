from django.contrib import admin
from .models import Encomenda, Transportadora, LogMovimentacao

admin.site.register(Encomenda)
admin.site.register(Transportadora)
admin.site.register(LogMovimentacao)