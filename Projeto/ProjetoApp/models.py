from django.db import models
from django.contrib.auth.models import User

class Postagem(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_postagem = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
