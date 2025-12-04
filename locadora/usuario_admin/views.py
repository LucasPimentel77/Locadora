from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView
from django.db.models import Q
from datetime import datetime, timedelta
from django.shortcuts import render
from reserva.models import Reserva
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .forms import AdminReservaForm
import calendar
from django.db.models import Count


def admin_required(function=None):
    """
    Decorator para views que requerem privilégios de admin
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_superuser or u.is_staff),
        login_url='/admin/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

@admin_required
# views_admin.py
def calendario_reservas(request):
    """
    Calendário com todas as reservas - TUDO processado na view
    """
    from datetime import datetime
    import calendar
    
    hoje = datetime.now().date()
    
    # Parâmetros para navegação
    try:
        ano = int(request.GET.get('ano', hoje.year))
        mes = int(request.GET.get('mes', hoje.month))
    except (ValueError, TypeError):
        ano = hoje.year
        mes = hoje.month
    
    # Calendário do mês
    cal = calendar.monthcalendar(ano, mes)
    
    # Buscar reservas do mês
    reservas_mes = Reserva.objects.filter(
        Q(data_retirada__year=ano, data_retirada__month=mes) |
        Q(data_devolucao__year=ano, data_devolucao__month=mes)
    ).select_related('usuario', 'grupo')
    
    # Processar TUDO na view
    semanas_processadas = []
    
    for semana_num, semana in enumerate(cal):
        semana_dias = []
        
        for dia in semana:
            if dia == 0:  # Dia vazio do calendário
                dia_info = {
                    'vazio': True,
                    'dia_numero': 0,
                    'contagem_reservas': 0,
                    'reservas': [],
                    'e_hoje': False,
                }
            else:
                # Filtrar reservas deste dia específico
                reservas_do_dia = []
                for reserva in reservas_mes:
                    # Verificar se é dia de retirada
                    if reserva.data_retirada.day == dia:
                        reservas_do_dia.append({
                            'reserva': reserva,
                            'tipo': 'retirada',
                            'classe': 'bg-primary',
                            'tooltip': f"{reserva.usuario} - {reserva.grupo.nome}",
                            'texto': f"#{reserva.id} - Retirada"
                        })
                    
                    # Verificar se é dia de devolução
                    if reserva.data_devolucao.day == dia:
                        reservas_do_dia.append({
                            'reserva': reserva,
                            'tipo': 'devolucao',
                            'classe': 'bg-success',
                            'tooltip': f"{reserva.usuario} - {reserva.grupo.nome}",
                            'texto': f"#{reserva.id} - Devolução"
                        })
                
                dia_info = {
                    'vazio': False,
                    'dia_numero': dia,
                    'contagem_reservas': len(reservas_do_dia),
                    'reservas': reservas_do_dia,
                    'e_hoje': (dia == hoje.day and mes == hoje.month and ano == hoje.year),
                }
            
            semana_dias.append(dia_info)
        
        semanas_processadas.append(semana_dias)
    
    # Mês anterior e próximo
    if mes > 1:
        mes_anterior = (ano, mes - 1)
    else:
        mes_anterior = (ano - 1, 12)
    
    if mes < 12:
        mes_proximo = (ano, mes + 1)
    else:
        mes_proximo = (ano + 1, 1)
    
    contexto = {
        'ano': ano,
        'mes': mes,
        'mes_nome': calendar.month_name[mes],
        'semanas': semanas_processadas,  # 🔥 TUDO já processado!
        'hoje': hoje,
        'mes_anterior': mes_anterior,
        'mes_proximo': mes_proximo,
        'total_reservas_mes': reservas_mes.count(),
    }
    
    return render(request, 'admin/calendario.html', contexto)

@admin_required
def gerenciar_reservas(request):
    """
    Lista todas as reservas com filtros para administração
    """
    from datetime import datetime, timedelta
    
    # Filtros
    status_filter = request.GET.get('status', 'todos')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    search_query = request.GET.get('q', '')
    
    reservas = Reserva.objects.exclude(
        status='inativo'
    ).select_related(
        'usuario', 'grupo'
    ).order_by('-data_criacao')
    
    # Aplicar filtros
    if status_filter != 'todos':
        reservas = reservas.filter(status=status_filter)
    
    if search_query:
        reservas = reservas.filter(
            Q(usuario__username__icontains=search_query) |
            Q(grupo__nome__icontains=search_query) |
            Q(id__icontains=search_query) |
            Q(usuario__email__icontains=search_query)
        )
    
    if data_inicio:
        try:
            data = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            reservas = reservas.filter(data_retirada__gte=data)
        except ValueError:
            pass
    
    if data_fim:
        try:
            data = datetime.strptime(data_fim, '%Y-%m-%d').date()
            reservas = reservas.filter(data_devolucao__lte=data)
        except ValueError:
            pass
    
    # Estatísticas
    total_reservas = reservas.count()
    reservas_por_status = Reserva.objects.values('status').annotate(
        total=Count('id')
    )
    
    # Cores para cada status
    cores_status = {
        'pendente': 'border-warning border-start border-5',
        'confirmada': 'border-success border-start border-5',
        'ativa': 'border-primary border-start border-5',
        'concluida': 'border-secondary border-start border-5',
        'cancelada': 'border-danger border-start border-5',
    }
    
    # Ícones para cada status
    icones_status = {
        'pendente': 'fas fa-clock text-warning',
        'confirmada': 'fas fa-check-circle text-success',
        'ativa': 'fas fa-car text-primary',
        'concluida': 'fas fa-flag-checkered text-secondary',
        'cancelada': 'fas fa-times-circle text-danger',
    }
    
    # Ações possíveis por status
    acoes_por_status = {
        'pendente': ['confirmar', 'cancelar', 'editar'],
        'confirmada': ['checkin', 'cancelar', 'editar'],
        'ativa': ['checkout', 'editar'],
        'concluida': ['visualizar', 'reabrir'],
        'cancelada': ['visualizar', 'reativar'],
    }
    
    contexto = {
        'reservas': reservas,
        'total_reservas': total_reservas,
        'status_filter': status_filter,
        'search_query': search_query,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'reservas_por_status': reservas_por_status,
        'cores_status': cores_status,
        'icones_status': icones_status,
        'acoes_por_status': acoes_por_status,
        'status_choices': Reserva.STATUS_CHOICES,
    }
    
    return render(request, 'admin/gerenciar_reservas.html', contexto)

@admin_required
def editar_reserva(request, reserva_id):
    """
    Editar uma reserva específica
    """
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    if request.method == 'POST':
        form = AdminReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, f'Reserva #{reserva.id} atualizada com sucesso!')
            return redirect('gerenciar_reservas')
    else:
        form = AdminReservaForm(instance=reserva)
    
    contexto = {
        'reserva': reserva,
        'form': form,
    }
    
    return render(request, 'admin/editar_reserva.html', contexto)