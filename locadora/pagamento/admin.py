from django.contrib import admin
from .models import Metodo, Cupom

# Register your models here.

class MetodoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao' ,'desconto', 'icone')
    
admin.site.register(Metodo, MetodoAdmin)

class CupomAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'desconto', 'data_validade', 'ativo')
admin.site.register(Cupom, CupomAdmin)