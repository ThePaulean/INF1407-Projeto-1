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
from django.urls import path
from ProjetoApp import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView


app_name = 'Projeto'

urlpatterns = [
    #URLS de usario
    path('',views.homeSec,name='sec-home'),
    path('accounts/login/', LoginView.as_view( template_name='registro/login.html',), name='sec-login'),
    path('accounts/profile/',views.pagina_admin, name='sec-paginaSecreta'),
    path('accounts/registro/',views.registro,name='sec-registro'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('sec-login'),), name='sec-logout'),
    #URLS de foruns
    path("foruns/", views.listar_foruns, name="listar_foruns"),
    path("foruns/create", views.criar_forum, name="criar_forum"),
    path("foruns/edit/<int:forum_id>", views.editar_forum, name="editar_forum"),
    path('excluir_forum/<int:forum_id>/', views.excluir_forum, name='excluir_forum'),
    #URLS das postagens 
    path('foruns/<int:forum_id>/postagens/', views.visualizar_e_criar_postagens, name='visualizar_e_criar_postagens'),
    path('editar_postagem/<int:postagem_id>/editar/', views.editar_postagem, name='editar_postagem'),    
    path('excluir_postagem/<int:postagem_id>/', views.excluir_postagem, name='excluir_postagem'),
    #URLS de Comentarios
    path('postagens/<int:postagem_id>/adicionar_comentario/', views.adicionar_comentario, name='adicionar_comentario'),
    path('excluir_comentario/<int:comentario_id>/', views.excluir_comentario, name='excluir_comentario'),
    path('editar_comentario/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    # URLS para troca de senha
    path('accounts/password_change/',PasswordChangeView.as_view(template_name='registro/password_change_form.html',success_url=reverse_lazy('sec-password_change_done'),), name='sec-password_change'),
    path('accounts/password_change_done/',PasswordChangeDoneView.as_view(template_name='registro/password_change_done.html',), name='sec-password_change_done'),
    path('accounts/password_reset/', 
         PasswordResetView.as_view(
            template_name='registro/password_reset_form.html', 
            success_url=reverse_lazy('sec-password_reset_done'),
            html_email_template_name='registro/password_reset_email.html',
            subject_template_name='registro/password_reset_subject.txt',
            from_email='webmaster@meslin.com.br',
        ), name='password_reset'),
    path('accounts/password_reset_done/', PasswordResetDoneView.as_view(template_name='registro/password_reset_done.html',
                                                                        ), name='sec-password_reset_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/',  
        PasswordResetConfirmView.as_view(
        template_name='registro/password_reset_confirm.html', 
        success_url=reverse_lazy('sec-password_reset_complete'),
        ), name='password_reset_confirm'),
    path('accounts/password_reset_complete/', PasswordResetCompleteView.as_view(
        template_name='registro/password_reset_complete.html'
        ), name='sec-password_reset_complete'),
    path('accounts/terminaRegistro/<int:pk>/', UpdateView.as_view( template_name='registro/user_form.html',success_url=reverse_lazy('sec-paginaSecreta'),model=User,fields=['first_name','last_name','email',],), name='sec-completaDadosUsuario'),
]
