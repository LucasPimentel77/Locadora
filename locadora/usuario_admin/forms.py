# locadora/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from reserva.models import Reserva
from carros.models import Carro, GrupoCarro
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminReservaForm(forms.ModelForm):
    """
    Formulário para edição de reservas por administradores
    (Apenas dados básicos, sem valor_final - o sistema calcula automaticamente)
    """
    class Meta:
        model = Reserva
        fields = [
            'status', 
            'usuario', 
            'grupo', 
            'data_retirada', 
            'data_devolucao'
            # 🔥 SEM valor_final - removido completamente
        ]
        widgets = {
            'data_retirada': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local', 
                    'class': 'form-control',
                    'placeholder': 'Data e hora de retirada'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'data_devolucao': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local', 
                    'class': 'form-control',
                    'placeholder': 'Data e hora de devolução'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_status'
            }),
            'usuario': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_usuario'
            }),
            'grupo': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_grupo'
            }),
        }
        labels = {
            'grupo': 'Grupo/Categoria do Carro',
            'data_retirada': 'Data/Hora de Retirada',
            'data_devolucao': 'Data/Hora de Devolução',
        }
        help_texts = {
            'grupo': 'Selecione a categoria/grupo do carro para a reserva',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar grupos ativos
        self.fields['grupo'].queryset = GrupoCarro.objects.filter(ativo=True)
        
        # Filtrar usuários ativos
        self.fields['usuario'].queryset = User.objects.filter(is_active=True)
    
    def clean(self):
        cleaned_data = super().clean()
        data_retirada = cleaned_data.get('data_retirada')
        data_devolucao = cleaned_data.get('data_devolucao')
        grupo = cleaned_data.get('grupo')
        
        # Validar datas
        if data_retirada and data_devolucao:
            if data_devolucao <= data_retirada:
                raise ValidationError({
                    'data_devolucao': 'A data de devolução deve ser posterior à data de retirada.'
                })
            
            if data_retirada < timezone.now():
                raise ValidationError({
                    'data_retirada': 'A data de retirada não pode ser no passado.'
                })
            
            # Verificar se período é muito longo (ex: mais de 30 dias)
            dias = (data_devolucao - data_retirada).days
            if dias > 30:
                raise ValidationError({
                    'data_devolucao': 'O período máximo de reserva é de 30 dias.'
                })
            
            # 🔥 CALCULAR E MOSTRAR VALOR ESTIMADO (apenas informação)
            if grupo and dias > 0:
                valor_estimado = grupo.preco_diaria * dias
                self.valor_estimado = valor_estimado
                self.dias = dias
        
        return cleaned_data