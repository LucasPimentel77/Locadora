from .models import Categoria

def popular_categorias():
    categorias = [
        {
            "nome": "Hatch/SUV",
            "slug": "hatch_suv",
            "icone_tipo": "🚙",
            "descricao": "Carros pequenos e médios, incluindo SUVs."
        },
        {
            "nome": "Sedan",
            "slug": "sedan",
            "icone_tipo": "🚗",
            "descricao": "Carros com mais conforto e espaço, ideais para viagens."
        },
        {
            "nome": "Picape",
            "slug": "picape",
            "icone_tipo": "🛻",
            "descricao": "Carros robustos, usados para trabalho ou aventura."
        },
        {
            "nome": "Esportivo",
            "slug": "esportivo",
            "icone_tipo": "🏎️",
            "descricao": "Carros de alta performance, velocidade e design."
        },
        {
            "nome": "Elétrico",
            "slug": "eletrico",
            "icone_tipo": "⚡",
            "descricao": "Carros movidos por energia elétrica, sustentáveis."
        },
        {
            "nome": "Van",
            "slug": "van",
            "icone_tipo": "🚐",
            "descricao": "Veículos para transporte de grupo de pessoas ou carga."
        },
        {
            "nome": "Moto",
            "slug": "moto",
            "icone_tipo": "🏍️",
            "descricao": "Motocicletas para viagens rápidas e práticas."
        }
    ]

    for categoria in categorias:
        # Verifica se a categoria já existe
        if not Categoria.objects.filter(slug=categoria['slug']).exists():
            Categoria.objects.create(
                nome=categoria['nome'],
                slug=categoria['slug'],
                icone_tipo=categoria['icone_tipo'],
                descricao=categoria['descricao']
            )
            print(f"Categoria '{categoria['nome']}' criada com sucesso.")
        else:
            print(f"A categoria '{categoria['nome']}' já existe.")
