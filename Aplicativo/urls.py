from django.urls import path,include
from Aplicativo.views import editar_aviso,update_com_id,update,add_admin,deletar_com_ids,deletar,sobre,login_viwes,tutoria,add_aluno,add_professor,retornar_index,eletivas,logout_viwes,add_eletivas,ver_eletiva,update_eletiva

urlpatterns = [
    path('', retornar_index,name='index'),
    path('login/',login_viwes ,name='login'),
    path('sobre/',sobre,name='sobre'),
    path('logout/',logout_viwes ,name='logout'),
    path('eletivas/', eletivas,name='eletivas'),
    path('add-eletiva/', add_eletivas,name='add-eletiva'),
    path('add/<str:tipo_de_user>', add_professor,name='add'),
    path('eletiva/<str:eletiva>',ver_eletiva,name='ver-eletiva'),
    path('update_eletiva/<int:id>',update_eletiva,name='update_eletiva'),
    path('update/<str:user>',update,name='update'),
    path('update/<str:user>/<int:id>',update_com_id,name='update_com_id'),
    path('add-aluno/',add_aluno,name='add-aluno'),
    path('add-admin/',add_admin,name='add-admin'),
    path('tutoria/',tutoria,name='tutoria'),
    path('editar_aviso/<int:id>',editar_aviso,name='editar_aviso'),
    path('tutoria/',tutoria,name='tutoria'),
    path('deletar/<str:user>',deletar,name='deletar'),
    path('deletar/<str:user>/<str:id>',deletar_com_ids,name='deletar_com_ids'),

    
]
