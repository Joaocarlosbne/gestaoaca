from django import forms
from .models import Estudante, Professor, Disciplina, Sala, Post, Aula, Curso
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.forms.widgets import Select

class EstudanteRegistroForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Estudante
        fields = ['numero_estudante', 'senha']  # add 'data_entrada' here

    def save(self, commit=True):
        user = super(EstudanteRegistroForm, self).save(commit=False)
        user.senha = make_password(self.cleaned_data['senha'])
        if commit:
            user.save()
        return user

class ProfessorRegistroForm(forms.ModelForm):
    senhap = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Professor
        fields = ['numero_funcionario', 'senhap']

    def save(self, commit=True):
        professor = super().save(commit=False)
        professor.senhap = make_password(self.cleaned_data['senhap'])
        professor.username = professor.numero_funcionario  # use numero_funcionario as username
        if commit:
            professor.save()
        return professor

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'codigo']

class LoginForm(forms.Form):
    numero_estudante = forms.CharField()
    senha = forms.CharField(widget=forms.PasswordInput)


class ProfessorLoginForm(forms.Form):
    numero_funcionario = forms.CharField()
    senhap = forms.CharField(widget=forms.PasswordInput)

class SalaForm(forms.ModelForm):  # define SalaForm here
    class Meta:
        model = Sala
        fields = ['numero', 'bloco']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'content']

from django import forms
from .models import Aula, Estudante

class AulaForm(forms.ModelForm):
    HORAS = [(f'{i:02d}:00', f'{i:02d}:00') for i in range(24)]
    DIAS_DA_SEMANA = [
        ('Segunda-feira', 'Segunda-feira'),
        ('Terça-feira', 'Terça-feira'),
        ('Quarta-feira', 'Quarta-feira'),
        ('Quinta-feira', 'Quinta-feira'),
        ('Sexta-feira', 'Sexta-feira'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]
    
    alunos = forms.ModelMultipleChoiceField(
        queryset=Estudante.objects.all(),
        widget=forms.SelectMultiple
    )
    hora_inicio = forms.TimeField(widget=forms.Select(choices=HORAS))
    hora_fim = forms.TimeField(widget=forms.Select(choices=HORAS))
    dia_da_semana = forms.CharField(widget=forms.Select(choices=DIAS_DA_SEMANA))
    sala = forms.ModelChoiceField(queryset=Sala.objects.all())  # Adicionado aqui

    class Meta:
        model = Aula
        fields = ['alunos', 'professor', 'disciplina', 'dia_da_semana', 'hora_inicio', 'hora_fim', 'sala']

class EstudanteForm(forms.ModelForm):
    class Meta:
        model = Estudante
        fields = ['numero_estudante', 'nome', 'matricula', 'curso', 'data_entrada', 'idade', 'endereco', 'cpf', 'rg', 'senha']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['cordenador', 'nome', 'formacao', 'numero_funcionario', 'senhap']

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['numero', 'bloco']

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'carga_horaria', 'tipo', 'descricao']
