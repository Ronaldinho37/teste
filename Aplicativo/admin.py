from django.contrib import admin
from.models import Alunos,Admins,Professores,Eletivas,Anuncio

# Register your models here.
admin.site.register(Professores)
admin.site.register(Alunos)
admin.site.register(Eletivas)
admin.site.register(Admins)
admin.site.register(Anuncio)