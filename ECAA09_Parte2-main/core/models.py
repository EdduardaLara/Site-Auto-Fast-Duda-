from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_cliente = models.BooleanField(default=False)
    is_oficina = models.BooleanField(default=False)

class Especialidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class PerfilOficina(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_oficina')
    especialidades = models.ManyToManyField(Especialidade)
    nome_oficina = models.CharField(max_length=200)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_oficina

class Problema(models.Model):
    STATUS_CHOICES = (
        ('ABERTO', 'Em Aberto'),
        ('ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDO', 'Concluído'),
    )

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problemas_criados')
    oficina = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicos_pegos')
    titulo = models.CharField(max_length=200)
    modelo_carro = models.CharField(max_length=100)
    descricao = models.TextField()
    
    # Campo de Imagem Adicionado Aqui
    imagem = models.ImageField(upload_to='problemas_imgs/', null=True, blank=True)

    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')

    def __str__(self):
        return f"{self.modelo_carro} - {self.titulo}"