from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.hashers import check_password, make_password
from django.utils.text import slugify
from django.conf import settings
from django.db import models
import os

class Aula(models.Model):
    alunos = models.ManyToManyField('Estudante', related_name='aulas_estudante')
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE)
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    sala = models.ForeignKey('Sala', on_delete=models.SET_NULL, null=True)  # Adicionado aqui
    dia_da_semana = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

class Professor(AbstractUser):
    cordenador = models.CharField(max_length=100, null=True)
    nome = models.CharField(max_length=100, null=True)
    formacao = models.CharField(max_length=100, null=True)
    numero_funcionario = models.CharField(max_length=255, unique=True)
    senhap = models.CharField(max_length=150)
    aulas = models.ManyToManyField('Aula', related_name='professores')

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="professor_groups",
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="professor_permissions",
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'numero_funcionario'
    PASSWORD_FIELD = 'senhap'

    class Meta:
        verbose_name = 'professor'
        verbose_name_plural = 'professors'
        db_table = 'auth_professor'

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return check_password(raw_password, self.senhap)

    @property
    def is_professor(self):
        return True

class Estudante(AbstractUser):
    username = None
    email = None
    numero_estudante = models.CharField(max_length=255, unique=True)
    nome = models.CharField(max_length=100, null=True)
    matricula = models.CharField(max_length=50, null=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, null=True)
    data_entrada = models.DateField(null=True)
    idade = models.IntegerField(null=True)
    endereco = models.CharField(max_length=400, null=True)
    cpf = models.CharField(max_length=14, null=True)
    rg = models.CharField(max_length=9, null=True)
    senha = models.CharField(max_length=150)
    aulas = models.ManyToManyField('Aula')

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="estudante_groups",
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="estudante_permissions",
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'numero_estudante'
    PASSWORD_FIELD = 'senha'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'estudante'
        verbose_name_plural = 'estudantes'
        db_table = 'auth_estudante'

    def __str__(self):
        return self.numero_estudante

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)

    @property
    def is_professor(self):
        return False

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    carga_horaria = models.IntegerField()
    tipo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=400)

    def __str__(self):
        return self.nome
    
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    professor = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True)
    sala = models.ForeignKey('Sala', on_delete=models.SET_NULL, null=True)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    def __str__(self):
        return self.nome

class Sala(models.Model):
    numero = models.CharField(max_length=10)
    bloco = models.CharField(max_length=1)

    def __str__(self):
        return self.bloco + self.numero
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    img_url = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.img_url:
            self.img_url = os.path.relpath(self.img_url, settings.STATIC_ROOT)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    