
from django.urls import path,include
from Aplicativo.views import login,add_aluno,add_professor,retornar_index,eletivas,logout,definir_carrossel,add_eletivas,ver_eletiva

urlpatterns = [
    path('', retornar_index,name='index'),
    path('login/',login ,name='login'),
    path('logout/',logout ,name='logout'),
    path('eletivas/', eletivas,name='eletivas'),
    path('definir_carrossel/', definir_carrossel,name='definir_carrossel'),
    path('add-eletiva/', add_eletivas,name='add-eletiva'),
    path('add-professor/<str:eletiva>', add_professor,name='add-professor'),
    path('eletiva/<str:eletiva>',ver_eletiva,name='ver-eletiva'),
    path('add-aluno/',add_aluno,name='add-aluno'),
    
]
