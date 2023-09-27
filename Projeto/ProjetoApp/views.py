from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import UpdateView
from .models import Postagem, Forum
from .forms import PostagemForm, ForumForm
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
            return redirect("ProjetoApp/listar_forum")
    else:
        form = ForumForm()
    return render(request, 'ProjetoApp/criar_forum.html', {'form': form})


def criar_postagem(request):
    if request.method == 'POST':
        form = PostagemForm(request.POST)
        if form.is_valid():
            postagem = form.save(commit=False)
            postagem.autor = request.user
            postagem.save()
            # Adicione uma mensagem de sucesso
            messages.success(request, 'A postagem foi criada com sucesso!')
            return redirect('visualizar_postagens')
    else:
        form = PostagemForm()
    return render(request, 'criar_postagem.html', {'form': form})


def visualizar_postagens(request, forum_id):
    # Buscar o fórum usando o forum_id
    forum = get_object_or_404(Forum, id=forum_id)

    # Filtra postagens que pertencem a esse forum
    postagens = Postagem.objects.filter(forum=forum)

    mensagens = messages.get_messages(request)    

    render_dict = {'postagens': postagens, 'mensagens': mensagens, "forum": forum}
    return render(request, 'ProjetoApp/visualizar_postagens.html', render_dict)


def excluir_postagem(request, postagem_id):
    # Obtenha a postagem a ser excluída
    postagem = get_object_or_404(Postagem, id=postagem_id)
    # Verifique se o usuário atual é o autor da postagem
    if request.user == postagem.autor:
        # Exclua a postagem
        postagem.delete()
        # Redirecione para a página de visualização de postagens ou para onde você preferir
        return redirect('visualizar_postagens')
    else:
        # Se o usuário não for o autor, você pode retornar uma mensagem de erro ou redirecioná-lo para outra página
        return redirect('visualizar_postagens')  # Ou outra página de sua escolha
    
@login_required
@user_passes_test(testa_acesso)

def forum(request):
    return render(request, 'ProjetoApp/homePageForum.html')
def paginaSecreta(request):
    return render(request, 'registro/paginaSecreta.html')



@login_required  # Isso garante que apenas usuários autenticados possam acessar as views
def pagina_admin(request):
    if request.user.is_superuser:
        return render(request, 'registro/paginaSecreta.html')
    else:
        return render(request, 'ProjetoApp/homePageForum.html')

@login_required
def pagina_usuario(request):
    if not request.user.is_superuser:
        return render(request, 'ProjetoApp/homePageForum.html')
    else:
        return render(request, 'registro/paginaSecreta.html')


class MeuUpdateView(UpdateView):
    def get(self, request, pk,*args,**kwargs):
        if request.user.id == pk:
            return super().get(request, pk, args, kwargs)
        else:
            return redirect('sec-home')
