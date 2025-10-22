from django.db import models

from categoria.models import Categoria

# Create your models here.
class GrupoCarro(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(max_length=500, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    preco_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Carro(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=500, blank=True)
    grupo = models.ForeignKey(GrupoCarro, on_delete=models.CASCADE)
    marca = models.CharField(max_length=100)
    ano = models.PositiveIntegerField()
    placa = models.CharField(max_length=20, unique=True)
    cor = models.CharField(max_length=50)
    disponivel = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='photos/carros/', blank=True)
    capacidade = models.PositiveIntegerField()
    combustivel = models.CharField(max_length=50, choices=[('gasolina', 'Gasolina'), ('etanol', 'Etanol'), ('flex', 'Flex')])
    capacidade = models.IntegerField(help_text="Número de passageiros")

    def __str__(self):
        return f"{self.nome} - {self.marca} ({self.ano})"