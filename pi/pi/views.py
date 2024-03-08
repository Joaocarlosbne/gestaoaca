from django.shortcuts import render, redirect, get_object_or_404
from .forms import EstudanteRegistroForm, ProfessorRegistroForm, DisciplinaForm, ProfessorLoginForm, PostForm, AulaForm
from .models import Estudante, Professor, Disciplina, Post, Aula
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .backends import ProfessorBackend, EstudanteBackend
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm
from django.forms.widgets import Select
from django.shortcuts import render
from .forms import SalaForm
from django.http import HttpResponseRedirect



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

    context = {
        'form': form,
        'posts': Post.objects.all().order_by('-date_posted'),
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
            user = authenticate(request, numero_funcionario=numero_funcionario, senhap=senhap)
            if user is not None:
                user.backend = f'{ProfessorBackend.__module__}.{ProfessorBackend.__name__}'  # specify the backend
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
            form.save()
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