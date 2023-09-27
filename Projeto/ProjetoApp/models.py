from django.db import models
from django.contrib.auth.models import User

class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, unique=True, )
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='forum_images/', null=True, blank=True)  # se voc� quiser adicionar uma imagem ao f�rum

    def __str__(self):
        return self.nome

class Postagem(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_postagem = models.DateTimeField(auto_now_add=True)
    
    # Forum ao qual a postagem pertence
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="postagens")

    def __str__(self):
        return self.titulo

