from django.db import models
from carros.models import GrupoCarro

# Create your models here.

class Reserva(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('ativa', 'Ativa'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    grupo = models.ForeignKey(GrupoCarro, on_delete=models.CASCADE)
    data_retirada = models.DateTimeField()
    data_devolucao = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    cupom = models.CharField(max_length=50, blank=True)
    desconto = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reserva #{self.id} - {self.carro}"