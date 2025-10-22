from django.shortcuts import get_object_or_404, render

from carros.models import Carro, GrupoCarro

from .models import Categoria

# Create your views here.

def categorias(request):
    return render(request, "categorias/categorias.html")

def categoria_detalhe(request, categoria_slug = None):
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    
    # Pega todos os subgrupos ativos desta categoria
    subgrupos = GrupoCarro.objects.filter(categoria=categoria, ativo=True)
    
    # Adiciona carros e informações extras para cada subgrupo
    subgrupos_com_carros = []
    for subgrupo in subgrupos:
        carros = Carro.objects.filter(grupo=subgrupo, disponivel=True)
        
        subgrupos_com_carros.append({
            'nome': subgrupo.nome,
            'descricao': subgrupo.descricao,
            'preco_diaria': subgrupo.preco_diaria,
            'total_carros': carros.count(),
            'carros': carros
        })
    
    # Marcas disponíveis para filtro
    marcas = Carro.objects.filter( 
        disponivel=True
    ).values_list('marca', flat=True).distinct()
    
    context = {
        'categoria': categoria,
        'subgrupos': subgrupos_com_carros,
        'marcas': marcas,
    }
    
    return render(request, 'categorias/categoria_detalhes.html', context)