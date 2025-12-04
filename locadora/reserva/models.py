from django.db import models
from carros.models import GrupoCarro
from pagamento.models import Pagamento
from django.contrib.auth.models import User

# Create your models here.

class Reserva(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('ativa', 'Ativa'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
        ('inativo', 'Inativo'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    grupo = models.ForeignKey(GrupoCarro, on_delete=models.CASCADE)
    data_retirada = models.DateTimeField()
    data_devolucao = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    pagamento = models.ForeignKey(Pagamento, on_delete=models.SET_NULL, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def set_status(self, novo_status):
        self.status = novo_status
        self.save()
    

    
    def __str__(self):
        return f"Reserva #{self.id} - {self.grupo.nome}"
    
    def duracao_dias(self):
        duracao = self.data_devolucao - self.data_retirada

        if duracao.days == 0:
            return 1
        if duracao.seconds <= 3600:
            return duracao.days
        else:
            return duracao.days + 1
        
    def valor_diarias(self):
        duracao = self.duracao_dias()
        valor_total = duracao * self.grupo.preco_diaria
        return valor_total

    def set_pagamento(self, pagamento):
        self.pagamento = pagamento
        self.save()