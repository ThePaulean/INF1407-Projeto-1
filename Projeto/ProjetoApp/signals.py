from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilUsuario

#Os signals permite que você execute código em resposta a eventos específicos, 
# como a criação de um novo usuário. Você precisará seguir estas etapas:
@receiver(post_save, sender=User)
def criar_ou_atualizar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)
    instance.perfilusuario.save()
