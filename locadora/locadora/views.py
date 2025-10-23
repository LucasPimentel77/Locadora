from datetime import datetime 
from django.utils import timezone
from django.shortcuts import render
from carros.models import Carro, GrupoCarro
from reserva.models import Reserva

def home(request):
    return render(request, 'home.html')

def alugar(request):
    # Gerar horários do dia (8h às 20h)
    horarios = [f"{h:02d}:00" for h in range(8, 21)]
    data_hoje = timezone.now().date()
    
    subgrupos_disponiveis = []
    subgrupos_indisponiveis = []
    
    if request.method == 'POST':
        data_retirada = request.POST.get('data_retirada')
        data_devolucao = request.POST.get('data_devolucao')
        hora_retirada = request.POST.get('hora_retirada')
        hora_devolucao = request.POST.get('hora_devolucao')

        if data_retirada and data_devolucao:
            # Converter para datetime
            dt_retirada = datetime.strptime(f"{data_retirada} {hora_retirada}", "%Y-%m-%d %H:%M")
            dt_devolucao = datetime.strptime(f"{data_devolucao} {hora_devolucao}", "%Y-%m-%d %H:%M")
            
            # Verificar disponibilidade por subgrupo
            for subgrupo in GrupoCarro.objects.filter(ativo=True):
                carros_disponiveis = verificar_disponibilidade(subgrupo, dt_retirada, dt_devolucao)
                
                subgrupo_data = {
                    'nome': subgrupo.nome,
                    'slug': subgrupo.slug,
                    'descricao': subgrupo.descricao,
                    'preco_diaria': subgrupo.preco_diaria,
                    'carros_disponiveis': carros_disponiveis
                }
                
                if carros_disponiveis > 0:
                    subgrupos_disponiveis.append(subgrupo_data)
                else:
                    subgrupos_indisponiveis.append(subgrupo_data)
    
    context = {
        'horarios': horarios,
        'data_hoje': data_hoje,
        'subgrupos_disponiveis': subgrupos_disponiveis,
        'subgrupos_indisponiveis': subgrupos_indisponiveis,
    }
    
    return render(request, 'reservas/alugar.html', context)

def verificar_disponibilidade(subgrupo, dt_retirada, dt_devolucao):
    """Verifica quantos carros estão disponíveis no período para o grupo"""
    # Total de carros no grupo
    total_carros = Carro.objects.filter(grupo=subgrupo, disponivel=True).count()
    
    # Reservas conflitantes para ESTE GRUPO
    reservas_conflitantes = Reserva.objects.filter(
        grupo=subgrupo,  # ← AGORA CORRETO: filtrando pelo grupo
        data_retirada__lt=dt_devolucao,
        data_devolucao__gt=dt_retirada,
        status__in=['confirmada', 'ativa']
    )
    
    # Número de reservas ativas neste período
    numero_reservas_ativas = reservas_conflitantes.count()
    
    # Carros disponíveis = total - reservas ativas
    carros_disponiveis = max(0, total_carros - numero_reservas_ativas)
    
    return carros_disponiveis