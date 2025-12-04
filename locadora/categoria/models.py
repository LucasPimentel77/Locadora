from django.db import models

from django.db.models import Min

# Create your models here.

class Categoria(models.Model):
    EMOJI_CHOICES = [
        ('', '---------'),
        ('🚙', '🚙 Hatch/SUV'),
        ('🚗', '🚗 Sedan'),
        ('🛻', '🛻 Picape'),
        ('🏎️', '🏎️ Esportivo'),
        ('⚡', '⚡ Elétrico'),
        ('🚐', '🚐 Van'),
        ('🏍️', '🏍️ Moto'),
        ('custom', '✏️ Personalizado (digite abaixo)'),
    ]
    

    icone_tipo = models.CharField(
        max_length=10,
        choices=EMOJI_CHOICES,
        default='',
        verbose_name="Tipo de Ícone"
    )
    icone_custom = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Emoji Personalizado",
        help_text="Digite qualquer emoji (ex: 🚀, ⚓, 🎯)"
    )
    nome = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    descricao = models.TextField(max_length=500, blank=True)
    imagem = models.ImageField(upload_to='photos/categorias/', blank=True)

    @property
    def menor_preco(self):
        """
        Retorna o menor preço entre todos os grupos desta categoria
        """
        from carros.models import GrupoCarro 
        
        resultado = GrupoCarro.objects.filter(
            categoria=self,
            ativo=True
        ).aggregate(menor_preco=Min('preco_diaria'))
        
        return resultado['menor_preco'] or 0
    
    def maior_preco(self):
        """
        Retorna o maior preço entre todos os grupos desta categoria
        """
        from carros.models import GrupoCarro 
        
        resultado = GrupoCarro.objects.filter(
            categoria=self,
            ativo=True
        ).aggregate(maior_preco=models.Max('preco_diaria'))
        
        return resultado['maior_preco'] or 0

    # Property para pegar o ícone correto
    @property
    def icone(self):
        if self.icone_tipo == 'custom':
            return self.icone_custom
        return self.icone_tipo

    def __str__(self):
        return self.nome