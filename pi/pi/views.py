from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from .forms import (
    EstudanteRegistroForm, 
    ProfessorRegistroForm, 
    DisciplinaForm, 
    ProfessorLoginForm, 
    PostForm, 
    AulaForm, 
    LoginForm, 
    EstudanteForm, 
    ProfessorForm, 
    SalaForm, 
    CursoForm,
    ProvaForm
)

from .models import (
    Estudante, 
    Professor, 
    Disciplina, 
    Post, 
    Aula, 
    Sala, 
    Nota, 
    Prova, 
    Presenca, 
    Curso
)

from .backends import ProfessorBackend, EstudanteBackend



def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form = PostForm()  # Clear the form
    else:
        form = PostForm()

    # Obtenha a aula que você quer usar aqui. Este é apenas um exemplo.
    aula = Aula.objects.first()

    context = {
        'form': form,
        'posts': Post.objects.all().order_by('-date_posted'),
        'aula': aula,  # Adicione a aula ao contexto
    }
    return render(request, 'home.html', context)

def registro_estudante(request):
    if request.method == 'POST':
        form = EstudanteRegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['senha'])
            user.save()
            user.backend = f'{EstudanteBackend.__module__}.{EstudanteBackend.__name__}'  # specify the backend
            login(request, user)
            return redirect('home')
    else:
        form = EstudanteRegistroForm()
    return render(request, 'registro_estudante.html', {'form': form})

def registro_professor(request):
    if request.method == 'POST':
        form = ProfessorRegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['senhap'])
            user.save()
            user.backend = f'{ProfessorBackend.__module__}.{ProfessorBackend.__name__}'  # specify the backend
            login(request, user)
            return redirect('home')
    else:
        form = ProfessorRegistroForm()
    return render(request, 'registro_professor.html', {'form': form})

def login_estudante(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            numero_estudante = form.cleaned_data.get('numero_estudante')
            senha = form.cleaned_data.get('senha')
            user = authenticate(request, numero_estudante=numero_estudante, password=senha)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login_estudante.html', {'form': form})

def login_professor(request):
    if request.method == 'POST':
        form = ProfessorLoginForm(request.POST)
        if form.is_valid():
            numero_funcionario = form.cleaned_data.get('numero_funcionario')
            senhap = form.cleaned_data.get('senhap')
            user = authenticate(request, username=numero_funcionario, password=senhap)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid login')
    else:
        form = ProfessorLoginForm()
    return render(request, 'login_professor.html', {'form': form})

def criar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            disciplina = form.save(commit=False)
            disciplina.horario_inicio = '00:00'
            disciplina.horario_fim = '00:00'
            disciplina.save()
            return redirect('home')
    else:
        form = DisciplinaForm()
    return render(request, 'criar_disciplina.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def criar_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect to the home page:
            return HttpResponseRedirect('/')
    else:
        form = SalaForm()

    return render(request, 'sala.html', {'form': form})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_details.html', {'post': post})

def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        content = request.POST['content']
        img_url = request.POST['img_url']
        new_post = Post(title=title, description=description, content=content, author=request.user, img_url=img_url)
        new_post.save()
        return redirect('home')
    else:
        return render(request, 'create_post.html')
    
def criar_aula(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AulaForm()
    return render(request, 'criar_aula.html', {'form': form})

def calendario(request):
    if request.user.is_authenticated:
        if request.user.is_professor:
            aulas = Aula.objects.filter(professor=request.user)
        else:
            aulas = Aula.objects.filter(aluno=request.user)
        return render(request, 'calendario.html', {'aulas': aulas})
    else:
        return redirect('login')

def ver_aulas(request):
    if request.user.is_authenticated:
        if request.user.is_professor:
            aulas = Aula.objects.filter(professor=request.user)
        else:
            aulas = Aula.objects.filter(alunos=request.user)
        dias_da_semana = AulaForm.DIAS_DA_SEMANA
        return render(request, 'ver_aulas.html', {'aulas': aulas, 'dias_da_semana': dias_da_semana})
    else:
        return redirect('login')
    
def editar(request):
    aulas = Aula.objects.all()
    disciplinas = Disciplina.objects.all()
    estudantes = Estudante.objects.all()
    posts = Post.objects.all()
    salas = Sala.objects.all()
    professores = Professor.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'editar.html', {
        'aulas': aulas,
        'disciplinas': disciplinas,
        'estudantes': estudantes,
        'posts': posts,
        'salas': salas,
        'professores': professores,
        'cursos' : cursos
    })

def editar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('editar')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'editar_disciplina.html', {'form': form})

def excluir_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)
    disciplina.delete()
    return redirect('editar')

def editar_estudante(request, id):
    estudante = get_object_or_404(Estudante, id=id)
    if request.method == 'POST':
        form = EstudanteForm(request.POST, instance=estudante)
        if form.is_valid():
            estudante.senha = make_password(request.POST.get('senha'))  # criando um hash da senha
            estudante.save()  # salva o objeto estudante, não o form
            return redirect('editar')
    else:
        form = EstudanteForm(instance=estudante)
    return render(request, 'editar_estudante.html', {'form': form})

def excluir_estudante(request, id):
    estudante = get_object_or_404(Estudante, id=id)
    if request.method == 'POST':
        estudante.delete()
        return redirect('editar')
    return render(request, 'excluir_estudante.html', {'estudante': estudante})

def editar_professor(request, id):
    professor = get_object_or_404(Professor, id=id)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            professor.senhap = make_password(request.POST.get('senhap'))  # criando um hash da senha
            professor.save()  # salva o objeto professor, não o form
            return redirect('editar')
    else:
        form = ProfessorForm(instance=professor)
    return render(request, 'editar_professor.html', {'form': form})

def excluir_professor(request, id):
    professor = get_object_or_404(Professor, id=id)
    if request.method == 'POST':
        professor.delete()
        return redirect('professores')
    return render(request, 'excluir_professor.html', {'professor': professor})

def editar_salas(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            return redirect('editar')
    else:
        form = SalaForm(instance=sala)
    return render(request, 'editar_sala.html', {'form': form})

def excluir_salas(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        sala.delete()
        return redirect('editar')
    return render(request, 'excluir_sala.html', {'sala': sala})

def editar_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('editar')
    else:
        form = PostForm(instance=post)
    return render(request, 'editar_post.html', {'form': form})

def excluir_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('editar')
    return render(request, 'excluir_post.html', {'post': post})

def editar_aula(request, id):
    aula = get_object_or_404(Aula, id=id)
    if request.method == 'POST':
        form = AulaForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            return redirect('editar')
    else:
        form = AulaForm(instance=aula)
    return render(request, 'editar_aula.html', {'form': form})

def excluir_aula(request, id):
    aula = get_object_or_404(Aula, id=id)
    if request.method == 'POST':
        aula.delete()
        return redirect('editar')
    return render(request, 'excluir_aula.html', {'aula': aula})

def get_aula_e_estudantes(aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    estudantes = aula.alunos.all()
    return aula, estudantes

def fazer_chamada(request, aula_id):
    aula = Aula.objects.get(id=aula_id)
    if request.method == 'POST':
        estudantes = aula.alunos.all()
        for estudante in estudantes:
            presente = request.POST.get(f'presente_{estudante.id}') == 'on'
            Presenca.objects.create(aula=aula, estudante=estudante, presente=presente)

        return redirect('ver_lista_presenca', aula_id=aula.id)
    else:
        estudantes = aula.alunos.all()
        return render(request, 'fazer_chamada.html', {'estudantes': estudantes, 'aula': aula})
    
def definir_notas(request, aula_id):
    aula = Aula.objects.get(id=aula_id)
    provas = Prova.objects.filter(aula=aula)
    if request.method == 'POST':
        estudantes = aula.alunos.all()
        prova_id = request.POST.get('prova')
        prova = Prova.objects.get(id=prova_id)
        for estudante in estudantes:
            nota = request.POST.get(f'nota_{estudante.id}', 0)
            nota = float(nota) if nota.strip() else 0
            nota_obj, created = Nota.objects.get_or_create(estudante=estudante, prova=prova, defaults={'valor': nota})
            nota_obj.valor = nota
            nota_obj.save()
        return redirect('editar')
    else:
        estudantes = aula.alunos.all()
        return render(request, 'definir_notas.html', {'estudantes': estudantes, 'provas': provas})

def definir_quantidade_provas(request, aula_id):
    aula = Aula.objects.get(id=aula_id)
    if request.method == 'POST':
        quantidade = request.POST.get('quantidade', 0)
        for _ in range(int(quantidade)):
            Prova.objects.create(aula=aula)
        return redirect('editar')
    else:
        return render(request, 'definir_quantidade_provas.html')

def definir_peso_provas(request, aula_id):
    aula = Aula.objects.get(id=aula_id)
    if request.method == 'POST':
        provas = Prova.objects.filter(aula=aula)
        for prova in provas:
            peso = request.POST.get(f'peso_{prova.id}', 0)
            prova.peso = peso
            prova.save()
        return redirect('editar')
    else:
        provas = Prova.objects.filter(aula=aula)
        return render(request, 'definir_peso_provas.html', {'provas': provas})

def calcular_media(request, aula_id):
    aula = Aula.objects.get(id=aula_id)
    if request.method == 'POST':
        estudantes = aula.alunos.all()
        for estudante in estudantes:
            media = estudante.media_notas(aula)
            estudante.media = media
            estudante.save()
        return redirect('editar')
    else:
        estudantes = aula.alunos.all()
        return render(request, 'calcular_media.html', {'estudantes': estudantes})

def marcar_reprovados(request, aula_id):
    aula = Aula.objects.get(id=aula_id)
    if request.method == 'POST':
        estudantes = aula.alunos.all()
        for estudante in estudantes:
            media = estudante.media_notas(aula)
            if media < 6 or estudante.porcentagem_presenca(aula) < 0.75:
                estudante.reprovado = True
                estudante.save()
        return redirect('editar')
    else:
        estudantes = aula.alunos.all()
        return render(request, 'marcar_reprovados.html', {'estudantes': estudantes})

def ver_lista_presenca(request, aula_id=None):
    if aula_id is not None:
        aulas = Aula.objects.filter(id=aula_id)
    else:
        aulas = Aula.objects.all()

    presencas_por_materia = {}

    for aula in aulas:
        presencas = Presenca.objects.filter(aula=aula).order_by('estudante__nome')
        if aula.disciplina.nome not in presencas_por_materia:
            presencas_por_materia[aula.disciplina.nome] = {}
        if aula.id not in presencas_por_materia[aula.disciplina.nome]:
            presencas_por_materia[aula.disciplina.nome][aula.id] = {}

        for presenca in presencas:
            if presenca.estudante.nome not in presencas_por_materia[aula.disciplina.nome][aula.id]:
                presencas_por_materia[aula.disciplina.nome][aula.id][presenca.estudante.nome] = []
            presencas_por_materia[aula.disciplina.nome][aula.id][presenca.estudante.nome].append(presenca)

    return render(request, 'ver_lista_presenca.html', {'presencas_por_materia': presencas_por_materia})
    
def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CursoForm()
    return render(request, 'criar_curso.html', {'form': form})

def cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos.html', {'cursos': cursos})

def gestao(request):
    # Certifique-se de que o usuário é um professor
    if not request.user.is_professor:
        return redirect('home')  # ou onde quer que você queira redirecionar usuários não professores

    # Buscar todas as aulas que o professor atual está lecionando
    aulas = Aula.objects.filter(professor=request.user)

    # Renderizar o template com as aulas
    return render(request, 'gestao.html', {'aulas': aulas})

def definir_prova(request, aula_id):
    if request.method == 'POST':
        form = ProvaForm(request.POST)
        if form.is_valid():
            prova = form.save(commit=False)
            prova.aula_id = aula_id
            prova.save()
            return redirect('gestao')
    else:
        form = ProvaForm()

    return render(request, 'definir_prova.html', {'form': form})

def ver_notas(request, aula_id):
    aula = Aula.objects.get(id=aula_id)
    estudantes = aula.alunos.all()
    dados = []

    for estudante in estudantes:
        provas_da_aula = Prova.objects.filter(aula=aula)
        notas = Nota.objects.filter(estudante=estudante, prova__in=provas_da_aula)
        media_ponderada = estudante.media_notas(aula)
        status = 'Aprovado' if estudante.esta_aprovado(aula) else 'Reprovado'
        dados.append({
            'estudante': estudante,
            'notas': notas,
            'media_ponderada': media_ponderada,
            'status': status,
            'rowspan': notas.count() + 1,
        })

    return render(request, 'ver_notas.html', {'dados': dados})

def professores(request):
    professores = Professor.objects.all()
    return render(request, 'professores.html', {'professores': professores})


def ver_minhas_notas(request):
    estudante = Estudante.objects.get(numero_estudante=request.user.numero_estudante)
    aulas = Aula.objects.filter(alunos=estudante)
    dados = []

    for aula in aulas:
        provas_da_aula = Prova.objects.filter(aula=aula)
        notas = Nota.objects.filter(estudante=estudante, prova__in=provas_da_aula)
        media_ponderada = estudante.media_notas(aula)
        status = 'Aprovado' if estudante.esta_aprovado(aula) else 'Reprovado'
        dados.append({
            'aula': aula,
            'estudante': estudante,
            'notas': notas,
            'media_ponderada': media_ponderada,
            'status': status,
            'rowspan': notas.count() + 1,
        })

    return render(request, 'ver_minhas_notas.html', {'dados': dados})