from django import forms
from .models import Comentario, Postagem, Forum

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['nome', 'descricao']

        
class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['titulo', 'conteudo']

        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']