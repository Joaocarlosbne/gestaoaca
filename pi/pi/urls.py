from django.contrib import admin
from django.urls import path
from . import views
from .views import home, registro_estudante, registro_professor, login_estudante, login_professor
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('registro_estudante/', views.registro_estudante, name='registro_estudante'),
    path('registro_professor/', views.registro_professor, name='registro_professor'),
    path('login_estudante/', views.login_estudante, name='login_estudante'),
    path('login_professor/', views.login_professor, name='login_professor'),
    path('criar_disciplina/', views.criar_disciplina, name='criar_disciplina'),
    path('logout/', views.logout_view, name='logout'),
    path('criar_sala/', views.criar_sala, name='criar_sala'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create_post/', views.create_post, name='create_post'),
    path('criar_aula/', views.criar_aula, name='criar_aula'),
    path('calendario/', views.calendario, name='calendario'),
    path('ver_aulas/', views.ver_aulas, name='ver_aulas'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)