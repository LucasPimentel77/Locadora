from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from reserva.models import Reserva
import json

@require_POST
@csrf_exempt
def atualizar_status_reserva(request, reserva_id):
    """
    API view para atualizar o status de uma reserva via AJAX
    """
    try:
        # Buscar a reserva
        reserva = Reserva.objects.get(id=reserva_id)
        
        # Verificar se o usuário tem permissão
        if reserva.usuario != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'Você não tem permissão para alterar esta reserva'
            }, status=403)
        
        # Ler dados da requisição
        data = json.loads(request.body)
        novo_status = data.get('status')
        
        # Validar status
        status_validos = ['pendente', 'confirmada', 'ativa', 'concluida', 'cancelada']
        if novo_status not in status_validos:
            return JsonResponse({
                'success': False,
                'error': f'Status inválido. Status válidos: {", ".join(status_validos)}'
            })
        
        # Lógica de transição de status
        transicoes_validas = {
            'pendente': ['confirmada', 'cancelada'],
            'confirmada': ['ativa', 'cancelada'],
            'ativa': ['concluida', 'cancelada'],
            'concluida': [],  # Não pode mudar de concluída
            'cancelada': []   # Não pode mudar de cancelada
        }
        
        # Verificar se a transição é válida
        if novo_status not in transicoes_validas[reserva.status]:
            return JsonResponse({
                'success': False,
                'error': f'Transição inválida: não é possível mudar de {reserva.status} para {novo_status}'
            })
        
        # Atualizar status e registrar data/hora
        reserva.status = novo_status
        
        # Registrar timestamps baseados no status
        reserva.data_atualizacao = timezone.now()
        
        reserva.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Status atualizado para {novo_status}',
            'reserva': {
                'id': reserva.id,
                'status': reserva.status,
                'status_display': reserva.get_status_display(),
            }
        })
        
    except Reserva.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Reserva não encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }, status=500)