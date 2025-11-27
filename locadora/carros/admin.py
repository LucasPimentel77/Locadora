from django.contrib import admin
from .models import Carro, GrupoCarro

# Register your models here.

class CarroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'cor', 'ano', 'grupo', 'imagem' ,'disponivel')
    search_fields = ('nome', 'marca', 'placa')
    list_filter = ('disponivel', 'grupo__categoria')

admin.site.register(Carro, CarroAdmin)

class GrupoCarroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_diaria', 'ativo')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)
    list_filter = ('categoria', 'ativo')

admin.site.register(GrupoCarro, GrupoCarroAdmin)
