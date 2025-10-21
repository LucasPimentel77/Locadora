from django.contrib import admin
from .models import Categoria

# Register your models here.
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'descricao', 'icone_tipo')
    prepopulated_fields = {'slug': ('nome',)}

fieldsets = ('Ícone', {
                'fields': ('icone_tipo', 'icone_custom'),
                'description': 'Escolha um emoji pré-definido ou selecione "Personalizado" para digitar qualquer emoji'
            }),



admin.site.register(Categoria, CategoriaAdmin)