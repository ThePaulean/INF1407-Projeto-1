from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import UpdateView
from .models import Postagem, Forum
from .forms import PostagemForm, ForumForm
from .models import Comentario
from .forms import ComentarioForm
from django.contrib import messages


#from django.http import HttpResponse
# Create your views here.
def home(request):
    #return HttpResponse("Olá mundo", content_type="text/plain")
    return render(request, 'ProjetoApp/home.html')


def homeSec(request):
    return render(request, "registro/homeSec.html")


def registro(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('sec-home')
    else:
        formulario = UserCreationForm()
    context = {'form': formulario, }
    return render(request, 'registro/registro.html', context)


# função que retorna True/False
def testa_acesso(user):
    # coloque aqui os testes que você precisar  
    if user.has_perm('contatos.change_pessoa'):
        return True
    else:
        return False
    

def listar_foruns(request):
    foruns = Forum.objects.all().order_by("nome")
    return render(request, "ProjetoApp/listar_foruns.html", {"foruns" : foruns})

@user_passes_test(lambda u: u.is_superuser)
def criar_forum(request):
    if request.method == "POST":
        form = ForumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_foruns")
    else:
        form = ForumForm()
    return render(request, 'ProjetoApp/criar_forum.html', {'form': form})

@login_required
def visualizar_e_criar_postagens(request, forum_id):
    # Obtenha o objeto de fórum com base no forum_id ou retorne um erro 404 se não existir
    forum = get_object_or_404(Forum, id=forum_id)
    
    # Obtenha todas as postagens relacionadas a este fórum
    postagens = Postagem.objects.filter(forum=forum)
    
    # Formulário para criar uma nova postagem
    if request.method == 'POST':
        form = PostagemForm(request.POST)
        if form.is_valid():
            postagem = form.save(commit=False)
            postagem.autor = request.user
            postagem.forum = forum  # Associe a postagem ao fórum correto
            postagem.save()
            return redirect('visualizar_e_criar_postagens', forum_id=forum_id)
    else:
        form = PostagemForm()

    context = {
        'forum': forum,
        'postagens': postagens,
        'form': form,
    }
    return render(request, 'ProjetoApp/visualizar_postagens.html', context)
@login_required

def editar_postagem(request, postagem_id):
    postagem = get_object_or_404(Postagem, id=postagem_id)

    if request.method == 'POST':
        form = PostagemForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
            return redirect('visualizar_e_criar_postagens', forum_id=postagem.forum.id)
    else:
        form = PostagemForm(instance=postagem)

    return render(request, 'ProjetoApp/editar_postagem.html', {'form': form, 'postagem': postagem})


def excluir_postagem(request, postagem_id):
    # Obtenha a postagem a ser excluída
    postagem = get_object_or_404(Postagem, id=postagem_id)
    forum_id = postagem.forum.id
    # Verifique se o usuário atual é o autor da postagem
    if request.user == postagem.autor:
        # Exclua a postagem
        postagem.delete()
        # Redirecione para a página de visualização de postagens ou para onde você preferir
        return redirect('visualizar_e_criar_postagens', forum_id=forum_id)
    else:
        # Se o usuário não for o autor, você pode retornar uma mensagem de erro ou redirecioná-lo para outra página
        return redirect('visualizar_e_criar_postagens', forum_id=forum_id)

def excluir_forum(request, forum_id):
    # Obtenha o fórum a ser excluído
    forum = get_object_or_404(Forum, id=forum_id)

    # Verifique se o usuário atual é o autor do fórum
    if request.user == forum.autor:
        # Exclua o fórum
        forum.delete()
        return redirect('listar_foruns', forum_id=forum_id)
    else:
    # Redirecione para a página de listagem de fóruns
        return redirect('listar_foruns',forum_id=forum_id)   

def adicionar_comentario(request, postagem_id):
    postagem = Postagem.objects.get(pk=postagem_id)  # Substitua "Postagem" pelo nome do seu modelo de postagem

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.postagem = postagem
            comentario.save()
            return redirect('visualizar_e_criar_postagens', forum_id=postagem.forum.id)  # Substitua 'visualizar_postagem' pela sua view de visualização de postagem
    else:
        form = ComentarioForm()

    return render(request, 'ProjetoApp/adicionar_comentario.html', {'form': form})

def excluir_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verifique se o usuário atual é o autor do comentário ou um administrador (ou outra lógica de autorização)
    if request.user == comentario.autor or request.user.is_superuser:
        comentario.delete()
        # Redirecione para onde você deseja após a exclusão do comentário
        return redirect('visualizar_e_criar_postagens', forum_id=comentario.postagem.forum.id)
    else:
        # Trate a situação em que o usuário não está autorizado a excluir o comentário
        # Pode ser uma mensagem de erro ou redirecionamento para outra página
        return redirect('visualizar_e_criar_postagens', forum_id=comentario.postagem.forum.id)
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if request.user != comentario.autor:
        # Se o usuário não for o autor do comentário, redirecione ou mostre uma mensagem de erro
        return redirect('visualizar_e_criar_postagens', forum_id=comentario.postagem.forum.id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('visualizar_e_criar_postagens', forum_id=comentario.postagem.forum.id)
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'ProjetoApp/editar_comentario.html', {'form': form, 'comentario': comentario})
@login_required
@user_passes_test(testa_acesso)

def forum(request):
    return render(request, 'ProjetoApp/listar_foruns.html')
def paginaSecreta(request):
    return render(request, 'registro/paginaSecreta.html')


@login_required  # Isso garante que apenas usuários autenticados possam acessar as views
def pagina_admin(request):
    if request.user.is_superuser:
        return render(request, 'registro/paginaSecreta.html')
    else:
        return render(request, 'ProjetoApp/listar_foruns.html')

@login_required
def pagina_usuario(request):
    if not request.user.is_superuser:
        return render(request, 'ProjetoApp/listar_foruns.html')
    else:
        return render(request, 'registro/paginaSecreta.html')


class MeuUpdateView(UpdateView):
    def get(self, request, pk,*args,**kwargs):
        if request.user.id == pk:
            return super().get(request, pk, args, kwargs)
        else:
            return redirect('sec-home')
