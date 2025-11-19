from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from reserva.models import Reserva

def cadastro(request):
    """View para cadastro de novo usuário"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'auth/cadastro.html', {'form': form})

def login_usuario(request):
    """View para login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})

def logout_usuario(request):
    """View para logout"""
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('home')

@login_required
def perfil(request):
    """Página de perfil do usuário"""
    # Estatísticas do usuário
    total_reservas = Reserva.objects.filter(usuario=request.user).count()
    reservas_confirmadas = Reserva.objects.filter(usuario=request.user, status='confirmada').count()
    ultimas_reservas = Reserva.objects.filter(usuario=request.user).order_by('-data_criacao')[:5]
    
    context = {
        'total_reservas': total_reservas,
        'reservas_confirmadas': reservas_confirmadas,
        'ultimas_reservas': ultimas_reservas,
    }
    
    return render(request, 'auth/perfil.html', context)

@login_required
def editar_perfil(request):
    """View para editar perfil do usuário"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    
    return redirect('perfil')