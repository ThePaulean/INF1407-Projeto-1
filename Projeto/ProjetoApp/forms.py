from django import forms
from .models import Postagem, Forum

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['nome', 'descricao']

class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['titulo', 'conteudo']
