from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Funcionario, Morador

admin.site.register(Funcionario, UserAdmin)
admin.site.register(Morador)