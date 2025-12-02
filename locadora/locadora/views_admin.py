from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView
from django.db.models import Q
from datetime import datetime, timedelta
from django.shortcuts import render
from reserva.models import Reserva
import calendar


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
def calendario_reservas(request):
    """
    Calendário com todas as reservas
    """
    hoje = datetime.now().date()
    
    # Parâmetros para navegação no calendário
    ano = request.GET.get('ano', hoje.year)
    mes = request.GET.get('mes', hoje.month)
    
    try:
        ano = int(ano)
        mes = int(mes)
    except (ValueError, TypeError):
        ano = hoje.year
        mes = hoje.month
    
    # Calendário do mês
    cal = calendar.monthcalendar(ano, mes)
    
    # Reservas do mês
    reservas_mes = Reserva.objects.filter(
        Q(data_retirada__year=ano, data_retirada__month=mes) |
        Q(data_devolucao__year=ano, data_devolucao__month=mes)
    ).select_related('grupo', 'usuario')
    
    # Agrupar reservas por dia
    reservas_por_dia = {}
    for reserva in reservas_mes:
        # Dias de retirada
        dia_retirada = reserva.data_retirada.day
        if dia_retirada not in reservas_por_dia:
            reservas_por_dia[dia_retirada] = []
        reservas_por_dia[dia_retirada].append({
            'reserva': reserva,
            'tipo': 'retirada',
            'classe': 'bg-primary'
        })
        
        # Dias de devolução
        dia_devolucao = reserva.data_devolucao.day
        if dia_devolucao not in reservas_por_dia:
            reservas_por_dia[dia_devolucao] = []
        reservas_por_dia[dia_devolucao].append({
            'reserva': reserva,
            'tipo': 'devolucao', 
            'classe': 'bg-success'
        })
    
    contexto = {
        'ano': ano,
        'mes': mes,
        'mes_nome': calendar.month_name[mes],
        'calendario': cal,
        'reservas_por_dia': reservas_por_dia,
        'hoje': hoje,
        'mes_anterior': (ano, mes-1) if mes > 1 else (ano-1, 12),
        'mes_proximo': (ano, mes+1) if mes < 12 else (ano+1, 1),
    }
    
    return render(request, 'admin/calendario.html', contexto)

@admin_required
def gerenciar_reservas(request):
    """
    Lista todas as reservas para administração
    """
    status_filter = request.GET.get('status', 'todos')
    search_query = request.GET.get('q', '')
    
    reservas = Reserva.objects.all().select_related('usuario', 'carro').order_by('-data_criacao')
    
    # Filtros
    if status_filter != 'todos':
        reservas = reservas.filter(status=status_filter)
    
    if search_query:
        reservas = reservas.filter(
            Q(usuario__username__icontains=search_query) |
            Q(carro__nome__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    contexto = {
        'reservas': reservas,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_reservas': reservas.count(),
    }
    
    return render(request, 'admin/gerenciar_reservas.html', contexto)

@admin_required 
def editar_reserva_admin(request, reserva_id):
    """
    Editar reserva de qualquer usuário (admin)
    """
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    if request.method == 'POST':
        form = AdminReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            reserva = form.save()
            messages.success(request, f'Reserva #{reserva.id} atualizada com sucesso!')
            return redirect('gerenciar_reservas')
    else:
        form = AdminReservaForm(instance=reserva)
    
    contexto = {
        'reserva': reserva,
        'form': form,
    }
    
    return render(request, 'admin/editar_reserva.html', contexto)

@admin_required
def relatorios(request):
    """
    Página de relatórios administrativos
    """
    # Estatísticas básicas
    total_reservas = Reserva.objects.count()
    reservas_ativas = Reserva.objects.filter(status='ativa').count()
    reservas_confirmadas = Reserva.objects.filter(status='confirmada').count()
    
    # Faturamento do mês
    hoje = datetime.now()
    faturamento_mes = Reserva.objects.filter(
        data_criacao__year=hoje.year,
        data_criacao__month=hoje.month,
        status__in=['confirmada', 'ativa', 'concluida']
    ).aggregate(total=Sum('valor_total'))['total'] or 0
    
    contexto = {
        'total_reservas': total_reservas,
        'reservas_ativas': reservas_ativas,
        'reservas_confirmadas': reservas_confirmadas,
        'faturamento_mes': faturamento_mes,
    }
    
    return render(request, 'admin/relatorios.html', contexto)