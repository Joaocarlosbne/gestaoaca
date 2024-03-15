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
    path('editar/', views.editar, name='editar'),
    path('editar_disciplina/<int:id>/', views.editar_disciplina, name='editar_disciplina'),
    path('excluir_disciplina/<int:id>/', views.excluir_disciplina, name='excluir_disciplina'),
    path('editar_estudante/<int:id>/', views.editar_estudante, name='editar_estudante'),
    path('excluir_estudante/<int:id>/', views.excluir_estudante, name='excluir_estudante'),
    path('excluir_professor/<int:id>/', views.excluir_professor, name='excluir_professor'),
    path('professores/', views.professores, name='professores'),
    path('ver_minhas_notas/', views.ver_minhas_notas, name='ver_minhas_notas'),
    path('editar_professor/<int:id>/', views.editar_professor, name='editar_professor'),
    path('editar_salas/<int:id>/', views.editar_salas, name='editar_sala'),
    path('excluir_sala/<int:id>/', views.excluir_salas, name='excluir_sala'),
    path('editar_post/<int:id>/', views.editar_post, name='editar_post'),
    path('excluir_post/<int:id>/', views.excluir_post, name='excluir_post'),
    path('editar_aula/<int:id>/', views.editar_aula, name='editar_aula'),
    path('excluir_aula/<int:id>/', views.excluir_aula, name='excluir_aula'),
    path('fazer_chamada/<int:aula_id>/', views.fazer_chamada, name='fazer_chamada'),
    path('definir_notas/<int:aula_id>/', views.definir_notas, name='definir_notas'),
    path('definir_quantidade_provas/<int:aula_id>/', views.definir_quantidade_provas, name='definir_quantidade_provas'),
    path('definir_peso_provas/<int:aula_id>/', views.definir_peso_provas, name='definir_peso_provas'),
    path('calcular_media/<int:aula_id>/', views.calcular_media, name='calcular_media'),
    path('marcar_reprovados/<int:aula_id>/', views.marcar_reprovados, name='marcar_reprovados'),
    path('cursos/criar/', views.criar_curso, name='criar_curso'),
    path('cursos/', views.cursos, name='cursos'),
    path('ver_lista_presenca/<int:aula_id>/', views.ver_lista_presenca, name='ver_lista_presenca'),
    path('gestao/', views.gestao, name='gestao'),
    path('definir_notas/<int:aula_id>/', views.definir_notas, name='definir_notas'),
    path('definir_quantidade_provas/<int:aula_id>/', views.definir_quantidade_provas, name='definir_quantidade_provas'),
    path('definir_peso_provas/<int:aula_id>/', views.definir_peso_provas, name='definir_peso_provas'),
    path('definir_prova/<int:aula_id>/', views.definir_prova, name='definir_prova'),
    path('ver_notas/<int:aula_id>/', views.ver_notas, name='ver_notas'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)