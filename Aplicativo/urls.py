from django.urls import path,include
from Aplicativo.views import sobre,tutoria,retornar_index,eletivas,logout_viwes,retornar_json

urlpatterns = [
    path('', retornar_index,name='index'),
    path('logout/',logout_viwes ,name='logout'),
    path('sobre/',sobre,name='sobre'),
    path('eletivas/', eletivas,name='eletivas'),
    # path('eletiva/<str:eletiva>',ver_eletiva,name='ver-eletiva'),
    path('tutoria/',tutoria,name='tutoria'),  

    
]
