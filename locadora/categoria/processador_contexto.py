from .models import Categoria

def get_categorias(request):
    categorias = Categoria.objects.all()
    return {'categorias': categorias}