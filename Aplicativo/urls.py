from django.urls import path,include
from Aplicativo.views import update_or_delete,editar_aviso,update_com_id,add_admin,deletar_com_ids,sobre,login_viwes,tutoria,add_aluno,add_professor,retornar_index,eletivas,logout_viwes,add_eletivas,ver_eletiva

urlpatterns = [
    path('', retornar_index,name='index'),
    path('sobre/',sobre,name='sobre'),
    path('eletivas/', eletivas,name='eletivas'),
    path('eletiva/<str:eletiva>',ver_eletiva,name='ver-eletiva'),
    path('tutoria/',tutoria,name='tutoria'),

    
]
