from django.db import models
from django.contrib.auth.models import User

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    membros = models.ManyToManyField(User, related_name='grupos_pertencentes', blank=True)
    def __str__(self):
        return self.nome

class Tarefas(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    concluida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tarefas',
        null=True,
        blank=True
    )

    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.SET_NULL,
        related_name='tarefas',
        null=True,
        blank=True

    )

    def __str__(self):
        nome_usuario = self.usuario.username if self.usuario else "Sem usuário"
        return f"{self.titulo} - {nome_usuario}"
