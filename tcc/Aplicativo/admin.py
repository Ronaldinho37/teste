from django.contrib import admin
from.models import Alunos,Admins,Professores,Eletivas

# Register your models here.
admin.site.register(Professores)
admin.site.register(Alunos)
admin.site.register(Eletivas)