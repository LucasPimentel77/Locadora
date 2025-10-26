from datetime import datetime 
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib import messages
from carros.models import Carro, GrupoCarro
from reserva.models import Reserva

def home(request):
    return render(request, 'home.html')

def alugar(request):
    horarios = [f"{h:02d}:00" for h in range(8, 21)]
    data_hoje = timezone.now().date()
    
    subgrupos_disponiveis = []
    subgrupos_indisponiveis = []
    
    # Variáveis para manter os dados do formulário
    data_retirada_form = ''
    data_devolucao_form = ''
    hora_retirada_form = ''
    hora_devolucao_form = ''
    cupom_form = ''
    
    if request.method == 'POST':
        print("=" * 70)
        print("🚀 PROCESSANDO FORMULÁRIO (POST)")
        
        data_retirada = request.POST.get('data_retirada')
        data_devolucao = request.POST.get('data_devolucao')
        hora_retirada = request.POST.get('hora_retirada')
        hora_devolucao = request.POST.get('hora_devolucao')
        cupom_form = request.POST.get('cupom', '')

        # Manter os valores do formulário
        data_retirada_form = data_retirada
        data_devolucao_form = data_devolucao
        hora_retirada_form = hora_retirada
        hora_devolucao_form = hora_devolucao


        print(f"📅 Datas recebidas: {data_retirada} {hora_retirada} → {data_devolucao} {hora_devolucao}")

        if data_retirada and data_devolucao:
            # Converter para datetime
            dt_retirada = datetime.strptime(f"{data_retirada} {hora_retirada}", "%Y-%m-%d %H:%M")
            dt_devolucao = datetime.strptime(f"{data_devolucao} {hora_devolucao}", "%Y-%m-%d %H:%M")
            
            # CONVERTER para timezone-aware
            dt_retirada = timezone.make_aware(dt_retirada)
            dt_devolucao = timezone.make_aware(dt_devolucao)

            # Verificar disponibilidade por subgrupo
            grupos_ativos = GrupoCarro.objects.filter(ativo=True)
            print(f"📋 Grupos ativos encontrados: {grupos_ativos.count()}")
            
            for subgrupo in grupos_ativos:
                carros_disponiveis = verificar_disponibilidade(subgrupo, dt_retirada, dt_devolucao)
                carros_subgrupo = Carro.objects.filter(grupo=subgrupo, disponivel=True)
                imagem = carros_subgrupo.first().imagem if carros_subgrupo.exists() else None

                subgrupo_data = {
                    'nome': subgrupo.nome,
                    'slug': subgrupo.slug,
                    'descricao': subgrupo.descricao,
                    'preco_diaria': subgrupo.preco_diaria,
                    'carros_disponiveis': carros_disponiveis,
                    'carros_subgrupo': carros_subgrupo,
                    'icone': subgrupo.categoria.icone,
                    'imagem': imagem.url if imagem else None,
                }
                
                if carros_disponiveis > 0:
                    subgrupos_disponiveis.append(subgrupo_data)
                    print(f"✅ ADICIONADO A DISPONÍVEIS: {subgrupo.nome} - {carros_disponiveis} carros")
                else:
                    subgrupos_indisponiveis.append(subgrupo_data)
                    print(f"❌ ADICIONADO A INDISPONÍVEIS: {subgrupo.nome}")

            print(f"\n🎯 RESUMO FINAL:")
            print(f"Disponíveis: {len(subgrupos_disponiveis)} grupos")
            print(f"Indisponíveis: {len(subgrupos_indisponiveis)} grupos")
            print("=" * 70)

    # SEMPRE passar os dados, independente do método
    context = {
        'horarios': horarios,
        'data_hoje': data_hoje,
        'subgrupos_disponiveis': subgrupos_disponiveis,
        'subgrupos_indisponiveis': subgrupos_indisponiveis,
        # Passar os dados do formulário para manter preenchido
        'data_retirada_form': data_retirada_form,
        'data_devolucao_form': data_devolucao_form,
        'hora_retirada_form': hora_retirada_form,
        'hora_devolucao_form': hora_devolucao_form,
        'cupom_form': cupom_form,
        # Variável para controle no template
        'foi_submetido': request.method == 'POST'
    }
    
    return render(request, 'reservas/alugar.html', context)

def verificar_disponibilidade(subgrupo, dt_retirada, dt_devolucao):
    """Verifica quantos carros estão disponíveis no período para o grupo"""
    print(f"🔍 ANALISANDO SUBGRUPO: {subgrupo.nome}")
    
    # Total de carros no grupo
    carros_no_grupo = Carro.objects.filter(grupo=subgrupo)
    total_carros = carros_no_grupo.count()
    print(f"  🚗 Total de carros no grupo: {total_carros}")
    
    # Carros disponíveis (não indisponíveis permanentemente)
    carros_disponiveis_base = carros_no_grupo.filter(disponivel=True).count()
    print(f"  🟢 Carros disponíveis (base): {carros_disponiveis_base}")
    
    # CONVERTER para timezone-aware (corrige o warning)
    if timezone.is_naive(dt_retirada):
        dt_retirada = timezone.make_aware(dt_retirada)
    if timezone.is_naive(dt_devolucao):
        dt_devolucao = timezone.make_aware(dt_devolucao)
    
    print(f"  ⏰ Datas (com timezone): {dt_retirada} → {dt_devolucao}")
    
    # Reservas conflitantes para ESTE GRUPO
    reservas_conflitantes = Reserva.objects.filter(
        grupo=subgrupo,
        data_retirada__lt=dt_devolucao,
        data_devolucao__gt=dt_retirada,
        status__in=['confirmada', 'ativa']
    )
    
    numero_reservas = reservas_conflitantes.count()
    print(f"  📅 Reservas conflitantes: {numero_reservas}")
    
    # Debug das reservas encontradas
    for reserva in reservas_conflitantes:
        print(f"    - Reserva #{reserva.id}: {reserva.data_retirada} a {reserva.data_devolucao} (Status: {reserva.status})")
    
    # Cálculo final
    carros_disponiveis_finais = max(0, carros_disponiveis_base - numero_reservas)
    print(f"  ✅ Carros disponíveis finais: {carros_disponiveis_finais}")
    
    return carros_disponiveis_finais

def escolher_grupo(request, slug_grupo):
    """Página para escolher o grupo e forma de pagamento"""
    try:
        grupo = GrupoCarro.objects.get(slug=slug_grupo, ativo=True)
        
        # Carros disponíveis neste grupo
        carros_disponiveis = Carro.objects.filter(grupo=grupo, disponivel=True)
        
        # Informações das formas de pagamento
        formas_pagamento = [
            {
                'tipo': 'pix',
                'nome': 'PIX',
                'descricao': 'Pagamento antecipado com 5% de desconto',
                'icone': 'fas fa-qrcode',
                'desconto': 5
            },
            {
                'tipo': 'cartao',
                'nome': 'Cartão de Crédito',
                'descricao': 'Pagamento antecipado em até 12x',
                'icone': 'fas fa-credit-card',
                'parcelas': 12
            },
            {
                'tipo': 'local',
                'nome': 'Pagamento no Local',
                'descricao': 'Pague na retirada do veículo',
                'icone': 'fas fa-store',
                'vantagem': 'Mais flexível'
            }
        ]
        
        context = {
            'grupo': grupo,
            'carros_disponiveis': carros_disponiveis,
            'formas_pagamento': formas_pagamento,
            'total_carros': carros_disponiveis.count(),
        }
        
        return render(request, 'reservas/escolher_grupo.html', context)
        
    except GrupoCarro.DoesNotExist:
        messages.error(request, "Grupo não encontrado.")
        return redirect('alugar')