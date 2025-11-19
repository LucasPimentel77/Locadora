from django.db import models
from decimal import Decimal

# Create your models here.
class Metodo(models.Model):
    TIPO_ICONE_CHOICES = [
        ('fas fa-qrcode', 'PIX'),
        ('fas fa-credit-card', 'Cartão'),
        ('fas fa-barcode', 'Boleto'),
        ('fab fa-paypal', 'PayPal'),
        ('fas fa-university', 'Transferência'),
        ('fas fa-money-bill-wave', 'Dinheiro'),
        ('fas fa-store', 'Local'),
    ]

    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=100, blank=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    icone = models.CharField(max_length=100, choices=TIPO_ICONE_CHOICES, default='fas fa-credit-card')


    def __str__(self):
        return self.nome
    
class Cupom(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2)
    data_validade = models.DateField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo

class Pagamento(models.Model):
    
    metodo = models.ForeignKey(Metodo, on_delete=models.CASCADE)
    cupom = models.ForeignKey(Cupom, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    taxas = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.metodo} - {self.valor}"
    
    def calcular_valor_final(self):
        """Calcula o valor final após desconto"""

        self.valor_final = self.valor

        if self.metodo.desconto > 0:
            desconto_valor = (self.metodo.desconto / 100) * self.valor_final
            self.valor_final = self.valor - desconto_valor
        if self.cupom:
            desconto_cupom = (self.cupom.desconto / 100) * self.valor_final
            self.valor_final -= desconto_cupom

        valor_taxa = (self.taxas / 100) * float(self.valor_final)
        self.valor_final += Decimal(valor_taxa)
        
        self.save()

    def desconto_metodo(self):
        return (self.metodo.desconto / 100) * self.valor
    
    def desconto_cupom(self):
        if self.cupom:
            return (self.cupom.desconto / 100) * self.valor
        return 0