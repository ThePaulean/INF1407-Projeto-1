from django import forms
from .models import Postagem

class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['titulo', 'conteudo']
