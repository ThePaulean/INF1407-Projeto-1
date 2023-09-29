from django.contrib import admin

# Register your models here.
from .models import PerfilUsuario

class PerfilUsuarioAdmin(admin.ModelAdmin):
    # Define como os detalhes do modelo serão exibidos no painel de administração
    list_display = ('usuario', 'cidade', 'estado', 'banido')

# Registra o modelo PerfilUsuario no painel de administração
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)