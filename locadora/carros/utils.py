from .models import GrupoCarro, Carro
from categoria.models import Categoria
from decimal import Decimal

def popular_grupos_de_carros():
    categorias = Categoria.objects.all()

    grupos_info = {
        'Hatch/SUV': [
            {"nome": "Hatch Compacto", "descricao": "Carro pequeno e ágil", "preco_diaria": Decimal('100.00'), "combustivel": 'flex'},
            {"nome": "SUV Executivo", "descricao": "SUV grande e confortável", "preco_diaria": Decimal('150.00'), "combustivel": 'diesel'},
            {"nome": "SUV Popular", "descricao": "SUV com preço acessível", "preco_diaria": Decimal('120.00'), "combustivel": 'flex'}
        ],
        'Sedan': [
            {"nome": "Sedan Básico", "descricao": "Carro para quem busca conforto", "preco_diaria": Decimal('130.00'), "combustivel": 'flex'},
            {"nome": "Sedan Luxo", "descricao": "Carro de luxo e sofisticação", "preco_diaria": Decimal('250.00'), "combustivel": 'flex'},
            {"nome": "Sedan Executivo", "descricao": "Carro confortável para viagens", "preco_diaria": Decimal('180.00'), "combustivel": 'eletrico'}
        ],
        'Picape': [
            {"nome": "Picape Pequena", "descricao": "Picape compacta e eficiente", "preco_diaria": Decimal('90.00'), "combustivel": 'diesel'},
            {"nome": "Picape Grande", "descricao": "Picape grande para trabalho pesado", "preco_diaria": Decimal('200.00'), "combustivel": 'diesel'},
            {"nome": "Picape Off-road", "descricao": "Picape com tração 4x4 para aventuras", "preco_diaria": Decimal('220.00'), "combustivel": 'flex'}
        ],
        'Esportivo': [
            {"nome": "Esportivo Compacto", "descricao": "Carro rápido e ágil", "preco_diaria": Decimal('300.00'), "combustivel": 'flex'},
            {"nome": "Esportivo Luxo", "descricao": "Carro esportivo de luxo", "preco_diaria": Decimal('500.00'), "combustivel": 'flex'},
            {"nome": "Esportivo High-performance", "descricao": "Carro de alta performance", "preco_diaria": Decimal('700.00'), "combustivel": 'eletrico'}
        ],
        'Elétrico': [
            {"nome": "Elétrico Compacto", "descricao": "Carro elétrico pequeno e econômico", "preco_diaria": Decimal('250.00'), "combustivel": 'eletrico'},
            {"nome": "Elétrico Luxo", "descricao": "Carro elétrico de luxo", "preco_diaria": Decimal('600.00'), "combustivel": 'eletrico'},
            {"nome": "Elétrico Familiar", "descricao": "Carro elétrico para a família", "preco_diaria": Decimal('350.00'), "combustivel": 'eletrico'}
        ],
        'Van': [
            {"nome": "Van Compacta", "descricao": "Van para transporte de pequenos grupos", "preco_diaria": Decimal('180.00'), "combustivel": 'flex'},
            {"nome": "Van Executiva", "descricao": "Van de luxo para viagens longas", "preco_diaria": Decimal('250.00'), "combustivel": 'diesel'},
            {"nome": "Van Família", "descricao": "Van confortável para famílias grandes", "preco_diaria": Decimal('220.00'), "combustivel": 'flex'}
        ],
        'Moto': [
            {"nome": "Moto Urbana", "descricao": "Moto compacta para o dia a dia", "preco_diaria": Decimal('50.00'), "combustivel": 'flex'},
            {"nome": "Moto Esportiva", "descricao": "Moto para quem busca velocidade", "preco_diaria": Decimal('120.00'), "combustivel": 'flex'},
            {"nome": "Moto Off-road", "descricao": "Moto para trilhas e aventuras", "preco_diaria": Decimal('150.00'), "combustivel": 'diesel'}
        ],
    }

    for categoria in categorias:
        # Para cada categoria, criamos 3 grupos de carros
        if categoria.nome in grupos_info:
            for grupo_info in grupos_info[categoria.nome]:
                # Verifica se o grupo já existe
                if not GrupoCarro.objects.filter(nome=grupo_info["nome"], categoria=categoria).exists():
                    GrupoCarro.objects.create(
                        categoria=categoria,
                        nome=grupo_info["nome"],
                        descricao=grupo_info["descricao"],
                        slug=grupo_info["nome"].lower().replace(" ", "_"),
                        preco_diaria=grupo_info["preco_diaria"],
                        combustivel=grupo_info["combustivel"]
                    )
                    print(f"Grupo '{grupo_info['nome']}' criado para a categoria '{categoria.nome}' com sucesso.")
                else:
                    print(f"O grupo '{grupo_info['nome']}' já existe na categoria '{categoria.nome}'.")


from random import choice, randint
import string

def gerar_placa():
    """Função para gerar uma placa aleatória"""
    return ''.join([choice(string.ascii_uppercase) for _ in range(3)]) + '-' + ''.join([choice(string.digits) for _ in range(4)])


def popular_carros_por_grupo():
    grupos = GrupoCarro.objects.all()

    # Dados para popular os carros
    carros_info = {
        'Hatch Compacto': [
            {"nome": "Fiat Uno", "descricao": "Carro pequeno e ágil, ideal para a cidade", "marca": "Fiat", "ano": 2015, "cor": "Branco", "capacidade": 5},
            {"nome": "Hyundai HB20", "descricao": "Carro popular, confiável e econômico", "marca": "Hyundai", "ano": 2018, "cor": "Prata", "capacidade": 5},
            {"nome": "Ford Ka", "descricao": "Carro compacto, econômico e perfeito para o dia a dia", "marca": "Ford", "ano": 2017, "cor": "Preto", "capacidade": 5},
        ],
        'SUV Executivo': [
            {"nome": "Jeep Compass", "descricao": "SUV confortável para viagens longas", "marca": "Jeep", "ano": 2020, "cor": "Preto", "capacidade": 5},
            {"nome": "Honda CR-V", "descricao": "SUV espaçoso e de alto desempenho", "marca": "Honda", "ano": 2021, "cor": "Prata", "capacidade": 5},
            {"nome": "Toyota RAV4", "descricao": "SUV com excelente desempenho e conforto", "marca": "Toyota", "ano": 2019, "cor": "Azul", "capacidade": 5},
        ],
        'SUV Popular': [
            {"nome": "Chevrolet Tracker", "descricao": "SUV compacto e acessível", "marca": "Chevrolet", "ano": 2020, "cor": "Cinza", "capacidade": 5},
            {"nome": "Renault Duster", "descricao": "SUV econômico e robusto", "marca": "Renault", "ano": 2018, "cor": "Branco", "capacidade": 5},
            {"nome": "Nissan Kicks", "descricao": "SUV com design moderno e conforto", "marca": "Nissan", "ano": 2021, "cor": "Preto", "capacidade": 5},
        ],
        'Sedan Básico': [
            {"nome": "Honda Civic", "descricao": "Carro sedã, confortável e confiável", "marca": "Honda", "ano": 2020, "cor": "Cinza", "capacidade": 5},
            {"nome": "Chevrolet Cruze", "descricao": "Sedã com ótimo custo-benefício", "marca": "Chevrolet", "ano": 2019, "cor": "Prata", "capacidade": 5},
            {"nome": "Volkswagen Virtus", "descricao": "Sedã espaçoso e ideal para viagens longas", "marca": "Volkswagen", "ano": 2021, "cor": "Azul", "capacidade": 5},
        ],
        'Sedan Luxo': [
            {"nome": "Toyota Corolla", "descricao": "Sedã executivo de luxo", "marca": "Toyota", "ano": 2022, "cor": "Azul", "capacidade": 5},
            {"nome": "Mercedes-Benz Classe C", "descricao": "Sedã de luxo com alto desempenho", "marca": "Mercedes-Benz", "ano": 2021, "cor": "Preto", "capacidade": 5},
            {"nome": "Audi A4", "descricao": "Sedã de luxo com design sofisticado", "marca": "Audi", "ano": 2022, "cor": "Branco", "capacidade": 5},
        ],
        'Picape Pequena': [
            {"nome": "Fiat Toro", "descricao": "Picape compacta e ideal para a cidade", "marca": "Fiat", "ano": 2021, "cor": "Vermelho", "capacidade": 2},
            {"nome": "Chevrolet S10", "descricao": "Picape para trabalho pesado", "marca": "Chevrolet", "ano": 2020, "cor": "Preto", "capacidade": 2},
            {"nome": "Mitsubishi L200", "descricao": "Picape robusta para grandes cargas", "marca": "Mitsubishi", "ano": 2021, "cor": "Cinza", "capacidade": 2},
        ],
        'Picape Grande': [
            {"nome": "Toyota Hilux", "descricao": "Picape grande e potente para aventuras", "marca": "Toyota", "ano": 2021, "cor": "Preto", "capacidade": 2},
            {"nome": "Ford Ranger", "descricao": "Picape com excelente capacidade de carga", "marca": "Ford", "ano": 2020, "cor": "Vermelho", "capacidade": 2},
            {"nome": "Chevrolet Silverado", "descricao": "Picape de grande porte com alta performance", "marca": "Chevrolet", "ano": 2022, "cor": "Branco", "capacidade": 2},
        ],
        'Picape Off-road': [
            {"nome": "Ford F-150", "descricao": "Picape para aventuras off-road", "marca": "Ford", "ano": 2021, "cor": "Azul", "capacidade": 2},
            {"nome": "Ram 1500", "descricao": "Picape de alto desempenho e versatilidade", "marca": "Ram", "ano": 2021, "cor": "Preto", "capacidade": 2},
            {"nome": "Nissan Frontier", "descricao": "Picape resistente e ideal para trilhas", "marca": "Nissan", "ano": 2020, "cor": "Prata", "capacidade": 2},
        ],
    }

    for grupo in grupos:
        if grupo.nome in carros_info:
            for carro_info in carros_info[grupo.nome]:
                # Gerar uma placa aleatória
                placa = gerar_placa()

                # Verifica se o carro já existe
                if not Carro.objects.filter(placa=placa, grupo=grupo).exists():
                    Carro.objects.create(
                        nome=carro_info["nome"],
                        descricao=carro_info["descricao"],
                        grupo=grupo,
                        marca=carro_info["marca"],
                        ano=carro_info["ano"],
                        placa=placa,
                        cor=carro_info["cor"],
                        capacidade=carro_info["capacidade"],
                        disponivel=True,  # Carro disponível por padrão
                    )
                    print(f"Carro '{carro_info['nome']}' criado para o grupo '{grupo.nome}'.")
                else:
                    print(f"O carro '{carro_info['nome']}' já existe no grupo '{grupo.nome}'.")
