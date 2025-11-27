from django.core.management.base import BaseCommand
from carros.models import Carro, GrupoCarro

class Command(BaseCommand):
    help = 'Popula o banco com carros de exemplo nas categorias existentes'

    def handle(self, *args, **options):

        # Dados dos carros por categoria (sem marca no nome)
        carros_por_categoria = {
            'hatch-automatico': [
                {'nome': 'Fiesta Automatic', 'marca': 'Ford', 'ano': 2023, 'placa': 'FIA2023', 'cor': 'Branco', 'capacidade': 5},
                {'nome': 'Polo TSI', 'marca': 'Volkswagen', 'ano': 2024, 'placa': 'POL2024', 'cor': 'Prata', 'capacidade': 5},
                {'nome': 'Onix Plus', 'marca': 'Chevrolet', 'ano': 2023, 'placa': 'ONX2023', 'cor': 'Preto', 'capacidade': 5},
            ],
            'suv-compacto': [
                {'nome': 'Renegade', 'marca': 'Jeep', 'ano': 2023, 'placa': 'REN2023', 'cor': 'Vermelho', 'capacidade': 5},
                {'nome': 'Creta', 'marca': 'Hyundai', 'ano': 2024, 'placa': 'CRE2024', 'cor': 'Branco', 'capacidade': 5},
                {'nome': 'Kicks', 'marca': 'Nissan', 'ano': 2023, 'placa': 'KIC2023', 'cor': 'Cinza', 'capacidade': 5},
            ],
            'suv-medio': [
                {'nome': 'RAV4', 'marca': 'Toyota', 'ano': 2023, 'placa': 'RAV2023', 'cor': 'Prata', 'capacidade': 5},
                {'nome': 'CR-V', 'marca': 'Honda', 'ano': 2024, 'placa': 'CRV2024', 'cor': 'Azul', 'capacidade': 5},
                {'nome': 'Escape', 'marca': 'Ford', 'ano': 2023, 'placa': 'ESC2023', 'cor': 'Preto', 'capacidade': 5},
            ],
            'suv-full-size': [
                {'nome': 'Tahoe', 'marca': 'Chevrolet', 'ano': 2024, 'placa': 'TAH2024', 'cor': 'Branco', 'capacidade': 8},
                {'nome': 'Expedition', 'marca': 'Ford', 'ano': 2023, 'placa': 'EXP2023', 'cor': 'Preto', 'capacidade': 8},
                {'nome': '4Runner', 'marca': 'Toyota', 'ano': 2024, 'placa': 'RUN2024', 'cor': 'Cinza', 'capacidade': 7},
            ],
            'picape-compacta': [
                {'nome': 'Maverick', 'marca': 'Ford', 'ano': 2024, 'placa': 'MAV2024', 'cor': 'Azul', 'capacidade': 5},
                {'nome': 'Santa Cruz', 'marca': 'Hyundai', 'ano': 2023, 'placa': 'SAN2023', 'cor': 'Cinza', 'capacidade': 5},
                {'nome': 'Frontier', 'marca': 'Nissan', 'ano': 2024, 'placa': 'FRO2024', 'cor': 'Branco', 'capacidade': 5},
            ],
            'picape-media': [
                {'nome': 'Hilux', 'marca': 'Toyota', 'ano': 2024, 'placa': 'HIL2024', 'cor': 'Prata', 'capacidade': 5},
                {'nome': 'Ranger', 'marca': 'Ford', 'ano': 2023, 'placa': 'RAN2023', 'cor': 'Azul', 'capacidade': 5},
                {'nome': 'S10', 'marca': 'Chevrolet', 'ano': 2024, 'placa': 'S102024', 'cor': 'Branco', 'capacidade': 5},
            ],
            'picape-premium': [
                {'nome': 'F-150 Raptor', 'marca': 'Ford', 'ano': 2024, 'placa': 'RAP2024', 'cor': 'Laranja', 'capacidade': 5},
                {'nome': '1500 TRX', 'marca': 'Ram', 'ano': 2023, 'placa': 'TRX2023', 'cor': 'Preto', 'capacidade': 5},
                {'nome': 'Silverado High Country', 'marca': 'Chevrolet', 'ano': 2024, 'placa': 'HIC2024', 'cor': 'Prata', 'capacidade': 5},
            ],
            'coupe-esportivo': [
                {'nome': '911 Carrera', 'marca': 'Porsche', 'ano': 2024, 'placa': 'POR2024', 'cor': 'Vermelho', 'capacidade': 4},
                {'nome': 'R8', 'marca': 'Audi', 'ano': 2023, 'placa': 'AUD2023', 'cor': 'Branco', 'capacidade': 2},
                {'nome': 'Corvette', 'marca': 'Chevrolet', 'ano': 2024, 'placa': 'COR2024', 'cor': 'Amarelo', 'capacidade': 2},
            ],
            'esportivo-economico': [
                {'nome': 'GR86', 'marca': 'Toyota', 'ano': 2023, 'placa': 'GR862023', 'cor': 'Azul', 'capacidade': 4},
                {'nome': 'BRZ', 'marca': 'Subaru', 'ano': 2024, 'placa': 'BRZ2024', 'cor': 'Vermelho', 'capacidade': 4},
                {'nome': 'Mustang EcoBoost', 'marca': 'Ford', 'ano': 2023, 'placa': 'MUS2023', 'cor': 'Preto', 'capacidade': 4},
            ],
            'supercarro': [
                {'nome': 'Aventador', 'marca': 'Lamborghini', 'ano': 2023, 'placa': 'LAM2023', 'cor': 'Laranja', 'capacidade': 2},
                {'nome': '488', 'marca': 'Ferrari', 'ano': 2024, 'placa': 'FER2024', 'cor': 'Vermelho', 'capacidade': 2},
                {'nome': '720S', 'marca': 'McLaren', 'ano': 2023, 'placa': 'MCL2023', 'cor': 'Laranja', 'capacidade': 2},
            ],
            'conversivel': [
                {'nome': 'MX-5 Miata', 'marca': 'Mazda', 'ano': 2024, 'placa': 'MX52024', 'cor': 'Vermelho', 'capacidade': 2},
                {'nome': 'Z4', 'marca': 'BMW', 'ano': 2023, 'placa': 'BMW2023', 'cor': 'Azul', 'capacidade': 2},
                {'nome': 'SL-Class', 'marca': 'Mercedes', 'ano': 2024, 'placa': 'SL2024', 'cor': 'Prata', 'capacidade': 2},
            ],
            'eletrico-compacto': [
                {'nome': 'Leaf', 'marca': 'Nissan', 'ano': 2023, 'placa': 'LEA2023', 'cor': 'Branco', 'capacidade': 5},
                {'nome': 'Bolt', 'marca': 'Chevrolet', 'ano': 2024, 'placa': 'BOL2024', 'cor': 'Azul', 'capacidade': 5},
                {'nome': 'i3', 'marca': 'BMW', 'ano': 2023, 'placa': 'I32023', 'cor': 'Cinza', 'capacidade': 4},
            ],
            'eletrico-familiar': [
                {'nome': 'Model Y', 'marca': 'Tesla', 'ano': 2024, 'placa': 'TES2024', 'cor': 'Branco', 'capacidade': 7},
                {'nome': 'Mustang Mach-E', 'marca': 'Ford', 'ano': 2023, 'placa': 'MAC2023', 'cor': 'Azul', 'capacidade': 5},
                {'nome': 'ID.4', 'marca': 'Volkswagen', 'ano': 2024, 'placa': 'ID42024', 'cor': 'Cinza', 'capacidade': 5},
            ],
            'eletrico-premium': [
                {'nome': 'Model S Plaid', 'marca': 'Tesla', 'ano': 2024, 'placa': 'PLA2024', 'cor': 'Preto', 'capacidade': 5},
                {'nome': 'Taycan', 'marca': 'Porsche', 'ano': 2023, 'placa': 'TAY2023', 'cor': 'Azul', 'capacidade': 4},
                {'nome': 'e-tron GT', 'marca': 'Audi', 'ano': 2024, 'placa': 'ETR2024', 'cor': 'Prata', 'capacidade': 4},
            ],
            'picape-eletrica': [
                {'nome': 'F-150 Lightning', 'marca': 'Ford', 'ano': 2024, 'placa': 'LIG2024', 'cor': 'Azul', 'capacidade': 5},
                {'nome': 'R1T', 'marca': 'Rivian', 'ano': 2023, 'placa': 'RIV2023', 'cor': 'Verde', 'capacidade': 5},
                {'nome': 'Cybertruck', 'marca': 'Tesla', 'ano': 2024, 'placa': 'CYB2024', 'cor': 'Prata', 'capacidade': 6},
            ],
        }

        # Criar carros
        total_carros = 0
        carros_criados = []
        
        for slug, carros in carros_por_categoria.items():
            try:
                grupo = GrupoCarro.objects.get(slug=slug)
                for carro_data in carros:
                    # Verificar se o carro já existe pela placa
                    if not Carro.objects.filter(placa=carro_data['placa']).exists():
                        carro = Carro.objects.create(
                            nome=carro_data['nome'],
                            grupo=grupo,
                            marca=carro_data['marca'],
                            ano=carro_data['ano'],
                            placa=carro_data['placa'],
                            cor=carro_data['cor'],
                            capacidade=carro_data['capacidade'],
                            disponivel=True
                        )
                        total_carros += 1
                        carros_criados.append(carro_data['nome'])
                        self.stdout.write(f"✅ Carro {carro_data['nome']} criado na categoria {grupo.nome}!")
                    else:
                        self.stdout.write(f"⚠️  Carro com placa {carro_data['placa']} já existe, pulando...")
            except GrupoCarro.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"❌ Categoria com slug '{slug}' não encontrada!")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 {total_carros} carros criados com sucesso!\n'
                f'📋 Categorias populadas: {len(carros_por_categoria)}'
            )
        )