from django.contrib.auth.backends import ModelBackend
from .models import Estudante, Professor

class EstudanteBackend(ModelBackend):
    def authenticate(self, request, numero_estudante=None, password=None, **kwargs):
        try:
            user = Estudante.objects.get(numero_estudante=numero_estudante)
            if user.check_password(password):
                return user
        except Estudante.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Estudante.objects.get(pk=user_id)
        except Estudante.DoesNotExist:
            return None

class ProfessorBackend(ModelBackend):
    def authenticate(self, request, numero_funcionario=None, senhap=None, **kwargs):
        try:
            professor = Professor.objects.get(numero_funcionario=numero_funcionario)
            if professor.check_password(senhap):
                return professor
        except Professor.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Professor.objects.get(pk=user_id)
        except Professor.DoesNotExist:
            return None