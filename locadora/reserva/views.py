from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from carros.models import GrupoCarro, Carro
from pagamento.models import Metodo, Cupom, Pagamento
from .models import Reserva
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
def escolher_grupo(request, slug_grupo):
    """Página para escolher o grupo e forma de pagamento"""
    try:
        grupo = GrupoCarro.objects.get(slug=slug_grupo, ativo=True)

        
        # Carros disponíveis neste grupo
        carros_disponiveis = Carro.objects.filter(grupo=grupo, disponivel=True)
        
        imagem = carros_disponiveis.first().imagem if carros_disponiveis.exists() else None
        
        # Se não há carros disponíveis, mostrar mensagem e redirecionar
        if not carros_disponiveis.exists():
            messages.warning(request, f"Não há carros disponíveis no grupo {grupo.nome} no momento.")
            return redirect('alugar')
        
        # Buscar métodos de pagamento do banco de dados
        metodos_pagamento = Metodo.objects.all()  # Pode adicionar .filter(ativo=True) se quiser
        
        # Cupons ativos (para sugestões)
        cupons_ativos = Cupom.objects.filter(ativo=True, data_validade__gte=timezone.now().date())
        
        context = {
            'grupo': grupo,
            'carros_disponiveis': carros_disponiveis,
            'metodos_pagamento': metodos_pagamento,
            'cupons_ativos': cupons_ativos,
            'total_carros': carros_disponiveis.count(),
            'imagem': imagem,
        }
        
        return render(request, 'reservas/escolher_grupo.html', context)
        
    except GrupoCarro.DoesNotExist:
        messages.error(request, "Grupo não encontrado ou indisponível.")
        return redirect('alugar')
    
def finalizar_reserva(request, slug_grupo):
    """Processa a finalização da reserva com pagamento"""
    if request.method == 'POST':
        try:
            grupo = GrupoCarro.objects.get(slug=slug_grupo, ativo=True)
            
            
            # Dados do formulário
            metodo_id = request.POST.get('metodo_pagamento')
            # O cupom vem do alugar.html, não do escolher_grupo.html
            cupom_codigo = request.session.get('cupom_aplicado', '')  # Buscar da sessão
            data_retirada = request.session.get('data_retirada')  # Buscar da sessão
            data_devolucao = request.session.get('data_devolucao')  # Buscar da sessão
            
            #==============TESTE=====================
            # metodo_id = 1
            # cupom_codigo = ''
            # data_retirada = "2025-11-15 10:00"
            # data_devolucao = "2025-11-20 14:00"
            
            # Validar dados obrigatórios
            if not metodo_id:
                messages.error(request, "Selecione uma forma de pagamento.")
                return redirect('home')
                # return redirect('escolher_grupo', slug_grupo=slug_grupo)
            
            if not data_retirada or not data_devolucao:
                messages.error(request, "Datas de retirada e devolução são obrigatórias.")
                return redirect('home')  # Redireciona para preencher datas
            
            # Buscar método de pagamento
            try:
                metodo = Metodo.objects.get(id=metodo_id)
            except Metodo.DoesNotExist:
                messages.error(request, "Método de pagamento inválido.")
                return redirect('escolher_grupo', slug_grupo=slug_grupo)
            
            # Buscar cupom se informado (da sessão)
            cupom = None
            if cupom_codigo:
                try:
                    cupom = Cupom.objects.get(
                        codigo__iexact=cupom_codigo, 
                        ativo=True, 
                        data_validade__gte=timezone.now().date()
                    )
                except Cupom.DoesNotExist:
                    messages.warning(request, f"Cupom {cupom_codigo} inválido ou expirado.")
            
           
            
            # Converter datas para datetime (já estão no formato correto da sessão)
            dt_retirada = timezone.make_aware(datetime.strptime(data_retirada, "%Y-%m-%d %H:%M"))
            dt_devolucao = timezone.make_aware(datetime.strptime(data_devolucao, "%Y-%m-%d %H:%M"))
            
            reserva = Reserva.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                grupo=grupo,
                data_retirada=dt_retirada,
                data_devolucao=dt_devolucao,
                status='pendente'
            )
            
            # Criar pagamento
            pagamento = Pagamento.objects.create(
                metodo=metodo,
                cupom=cupom,
                valor=reserva.valor_diarias(),
            )
            pagamento.calcular_valor_final()

            reserva.set_pagamento(pagamento)
            
            
        
            
            # Limpar dados da sessão
            if 'cupom_aplicado' in request.session:
                del request.session['cupom_aplicado']
            if 'data_retirada' in request.session:
                del request.session['data_retirada']
            if 'data_devolucao' in request.session:
                del request.session['data_devolucao']
            
            # Mensagem de sucesso
            messages.success(
                request, 
                f"Reserva #{reserva.id} confirmada! " +
                f"Valor total: R$ {pagamento.valor_final:.2f}. " +
                "Verifique seu e-mail para mais detalhes."
            )
            
            print(f' reserva id: {reserva.id} ')
            return redirect('detalhes_reserva', reserva_id=reserva.id)
            
        except GrupoCarro.DoesNotExist:
            messages.error(request, "Grupo não encontrado.")
            return redirect('home')
        # except Exception as e:
        #     messages.error(request, f"Erro ao processar reserva: {str(e)}")
        #     return redirect('escolher_grupo', slug_grupo=slug_grupo)
    
    # Se não for POST, redirecionar
    messages.warning(request, "Método não permitido.")
    return redirect('home')

def detalhes_reserva(request, reserva_id):
    """Mostra os detalhes da reserva confirmada"""
    try:
        reserva = Reserva.objects.get(id=reserva_id)
        carros_grupo = Carro.objects.filter(grupo=reserva.grupo)
        imagem = carros_grupo.first().imagem if carros_grupo.exists() else None
        capacidade = carros_grupo.first().capacidade if carros_grupo.exists() else None
        context = {
            'reserva': reserva,
            'imagem': imagem,
            'capacidade': capacidade,
        }
        return render(request, 'reservas/detalhes_reserva.html', context)
    except Reserva.DoesNotExist:
        messages.error(request, "Reserva não encontrada.")
        return redirect('home')
    

@require_POST
@csrf_exempt
def verificar_cupom(request):
    """API para verificar se um cupom é válido"""
    try:
        print("🔍 Iniciando verificação de cupom...")
        
        # Ler dados JSON
        data = json.loads(request.body.decode('utf-8'))
        cupom_codigo = data.get('cupom', '').strip().upper()
        
        print(f"🔍 Cupom recebido: '{cupom_codigo}'")
        
        if not cupom_codigo:
            return JsonResponse({
                'valido': False,
                'mensagem': 'Digite um código de cupom.'
            })
        
        # ✅ CORREÇÃO: Import do app correto
        from pagamento.models import Cupom
            
        # Buscar cupom no banco de dados
        try:
            cupom = Cupom.objects.get(
                codigo__iexact=cupom_codigo,
                ativo=True
            )
            
            print(f"✅ Cupom encontrado: {cupom.codigo}")
            
            # Verificar validade
            if cupom.data_validade < timezone.now().date():
                print(f"❌ Cupom expirado: {cupom.data_validade}")
                return JsonResponse({
                    'valido': False,
                    'mensagem': 'Cupom expirado.'
                })
            
            print(f"✅ Cupom válido: {cupom.codigo} - {cupom.desconto}%")
            
            # Calcular desconto
            valor_total = 100.00
            desconto_percentual = float(cupom.desconto)
            valor_desconto = (desconto_percentual / 100) * valor_total
            
            return JsonResponse({
                'valido': True,
                'mensagem': f'Cupom válido! {cupom.desconto}% de desconto aplicado.',
                'desconto_percentual': desconto_percentual,
                'valor_desconto': round(valor_desconto, 2),
                'desconto_aplicado': True
            })
            
        except Cupom.DoesNotExist:
            print(f"❌ Cupom não encontrado: {cupom_codigo}")
            return JsonResponse({
                'valido': False,
                'mensagem': 'Cupom inválido.'
            })
            
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        print(traceback.format_exc())
        return JsonResponse({
            'valido': False,
            'mensagem': 'Erro interno do servidor.'
        })

@login_required
def minhas_reservas(request):
    """View para listar reservas do usuário logado"""
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    context = {
        'reservas': reservas
    }
    return render(request, 'reservas/minhas_reservas.html', context)

@login_required
def detalhes_minha_reserva(request, reserva_id):
    """View para detalhes de uma reserva específica do usuário"""
    try:
        reserva = Reserva.objects.get(id=reserva_id, usuario=request.user)
    except Reserva.DoesNotExist:
        messages.error(request, "Reserva não encontrada.")
        return redirect('minhas_reservas')
    
    context = {
        'reserva': reserva
    }
    return render(request, 'reservas/minhas_reserva.html', context)