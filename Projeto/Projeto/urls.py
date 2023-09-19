"""
URL configuration for Projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ProjetoApp import views
#from MeuSite import views
from django.urls.conf import include
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView

app_name = 'Projeto'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls), #remover pois se nao podem atacar o site, da acesso a parte de adminstrador
    path('',views.home, name='inicio'),
    path('accounts/',views.homeSec,name='sec-home'),
    path('accounts/login/', LoginView.as_view( template_name='registro/login.html',), name='sec-login'),
    path('accounts/profile/forum/',views.pagina_usuario,name='forum'),
    path('accounts/profile/',views.pagina_admin, name='sec-paginaSecreta'),
    path('accounts/registro/',views.registro,name='sec-registro'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('sec-login'),), name='sec-logout'),
    path('criar_postagem/', views.criar_postagem, name='criar_postagem'),
    path('visualizar_postagens/', views.visualizar_postagens, name='visualizar_postagens'),
    path('excluir_postagem/<int:postagem_id>/', views.excluir_postagem, name='excluir_postagem'),

    path('accounts/password_change/',PasswordChangeView.as_view(template_name='registro/password_change_form.html',success_url=reverse_lazy('sec-password_change_done'),), name='sec-password_change'),
    path('accounts/password_change_done/',PasswordChangeDoneView.as_view(template_name='registro/password_change_done.html',), name='sec-password_change_done'),
    path('accounts/terminaRegistro/<int:pk>/', UpdateView.as_view( template_name='registro/user_form.html',success_url=reverse_lazy('sec-paginaSecreta'),model=User,fields=['first_name','last_name','email',],), name='sec-completaDadosUsuario'),
    
]
