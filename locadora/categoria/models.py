from django.db import models

# Create your models here.

class Categoria(models.Model):
     # Choices principais + opção customizada
    EMOJI_CHOICES = [
        ('', '---------'),  # Opção vazia
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

    # Property para pegar o ícone correto
    @property
    def icone(self):
        if self.icone_tipo == 'custom':
            return self.icone_custom
        return self.icone_tipo

    def __str__(self):
        return self.nome