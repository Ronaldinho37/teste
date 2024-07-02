from django.shortcuts import render,redirect
from .forms import LoginForm,AddEletivaForm
from django.http import HttpResponse
from .models import Alunos,Admins,Professores,ImgCarrossel,Eletivas
from django.contrib import messages
import os


# ImgCarrossel.objects.all().delete()
#1920 x 695 
# Create your views here.

#como codificar palavras
import rsa
(publickey, privatekey) = rsa.newkeys(100)
m = "oi".encode('utf8')
ciphertext = rsa.encrypt(m, publickey)
m2 = rsa.decrypt(ciphertext, privatekey)
print(ciphertext)

user=[None]
def excluir_imagem(dir,model):
    #variável que guarda as imagens que estão sendo utilizadas
    imagens_usuarios = []
    #variável que guarda todas imagens da pasta media
    s = os.listdir(f'{os.getcwd()}/media/{dir}')
    #adiciona as imagens que estão sendo usadas á variável imagens_usuarios
    if dir == "img_carrosssel":
        for i in model:
            if i['img1'] not in imagens_usuarios:
                img = i['img1'].replace(f'{dir}/','')
                imagens_usuarios.append(img)
            if i['img2'] not in imagens_usuarios:
                img = i['img2'].replace(f'{dir}/','')
                imagens_usuarios.append(img)
            if i['img3'] not in imagens_usuarios:
                img = i['img3'].replace(f'{dir}/','')
                imagens_usuarios.append(img)
    else:
        for i in model:
            if i['imagem'] not in imagens_usuarios:
                img = i['imagem'].replace(f'{dir}/','')
                imagens_usuarios.append(img)
    #deleta as imagens que não estão sendo usadas: se a imagem não estiver em imagens_usuarios então a delete
    for i in s:
        if i not in imagens_usuarios:
            os.remove(f'{os.getcwd()}/media/{dir}/{i}')
         
   
    return

def retornar_index(request):
    dados = {}
    dados['user'] = user[0]
    dados['img_carrossel'] = ImgCarrossel.objects.all()[:1]
    print(ImgCarrossel.objects.all()[:1])
    return render(request,'index.html',dados)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #irá checar se o usuário é um admin
            adms = Admins.objects.all().values()
            for i in adms:
                if i['nome'].lower() == form.cleaned_data.get('nome').lower() and i['senha'] == form.cleaned_data.get('senha'):
                    user.clear()
                    user.append('admin')
                    return redirect(retornar_index)
            #irá checar se o usuário é um professor
            professor = Professores.objects.all().values()
            for i in professor:
                if i['nome'].lower() == form.cleaned_data.get('nome').lower() and i['senha'] == form.cleaned_data.get('senha'):
                    user.clear()
                    user.append('professor')
                    return redirect(retornar_index)
            #irá checar se o usuário é um alunos
            alunos = Alunos.objects.all().values()
            for i in alunos:
                if i['nome'].lower() == form.cleaned_data.get('nome').lower() and i['senha'] == form.cleaned_data.get('senha'):
                    user.clear()
                    user.append('aluno')
                    return redirect(retornar_index)
            messages.info(request,"Usuário ou senha inválidos!")
            dados = {}
            dados['form'] = LoginForm()
            return render(request,'login.html',dados)
    else:
        dados = {}
        dados['form'] = LoginForm()
        return render(request,'login.html',dados)

def eletivas(request):
    dados = {}
    dados['eletivas'] = Eletivas.objects.all().values()
    return render(request,'eletivas.html',dados)

def logout(request):
    user.clear()
    user.append(None)
    return redirect(retornar_index)

def definir_carrossel(request):
    if request.method == 'POST':
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        ImgCarrossel.objects.all().delete()
        carrossel = ImgCarrossel(img1=img1,img2=img2,img3=img3)
        carrossel.save()
        model = ImgCarrossel.objects.all().values()
        excluir_imagem("img_carrosssel",model)

        return redirect(retornar_index)
    else:
        return render(request,'imgcarrossel.html')

def add_eletivas(request):
    if request.method == 'POST':
        form = AddEletivaForm(request.POST, request.FILES)
        if form.is_valid():
            new = Eletivas(titulo=form.cleaned_data.get('titulo'),descricao=form.cleaned_data.get('descricao'),imagem=form.cleaned_data.get("imagem"))
            new.save()
            model = Eletivas.objects.all().values()
            excluir_imagem("img_eletivas",model)
            return redirect(add_professor,eletiva=form.cleaned_data.get('titulo'))
    else:
        dados = {}
        dados['form'] = AddEletivaForm()
        return render(request,'addeletiva.html',dados)

def ver_eletiva(request,eletiva):
    dados = {}
    dados['id'] = 1
    alunos = Alunos.objects.all().values()
    professores = Professores.objects.all().values()
    pode_ir = []
    for i in alunos:
        if i['eletiva'] == eletiva:
            pode_ir.append(True)
            break
    if len(pode_ir) == 0:
        pode_ir.append(False)
    for i in professores:
        if i['eletiva'] == eletiva:
            pode_ir.append(True)
            break  
    if len(pode_ir) == 1:
        pode_ir.append(False)
    
    if pode_ir[0] == True and pode_ir[1] == True:
        dados['alunos'] = Alunos.objects.filter(eletiva=eletiva)
        dados['professor'] = Professores.objects.get(eletiva=eletiva)
        return  render(request,'eletiva.html',dados)
    elif pode_ir[0] == False and pode_ir[1] == True:
        messages.info(request,'Nenhum aluno nesta eletiva')
        dados['professor'] = Professores.objects.get(eletiva=eletiva)
        return  render(request,'eletiva.html',dados)
    elif pode_ir[0] == True and pode_ir[1] == False:
        messages.info(request,'Nenhum professor nesta eletiva')
        dados['alunos'] = Alunos.objects.all().filter(eletiva=eletiva)
        return  render(request,'eletiva.html',dados)
    else:
        messages.info(request,'Nenhum aluno e professor nesta eletiva')
        return  render(request,'eletiva.html',dados)
    

def add_professor(request,eletiva):
    if request.method == 'POST':
        select = request.POST.get('eletiva')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        form = [select,nome,email,senha]
        for i in form:
            if i == '':
                dados = {}
                dados['eletivas'] = Eletivas.objects.all().values()
                messages.info(request,'Nenhum campo pode ser deixado em branco')
                return render(request,'addprofessor.html',dados)
        professor = Professores(eletiva=select,nome=nome,email=email,senha=senha)
        professor.save()
        return redirect(eletivas)
    else:
        dados={}
        dados['eletiva'] = eletiva
        return render(request,'addprofessor.html',dados)

def add_aluno(request):
    if request.method == 'POST':
        aluno = Alunos(serie=request.POST.get('serie'),nome=request.POST.get('nome'),email=request.POST.get('email'),senha=request.POST.get('senha'),eletiva=request.POST.get('select'))
        aluno.save()
        return redirect(ver_eletiva,eletiva=request.POST.get('select'))
    else:
        dados={}
        dados['eletivas'] = Eletivas.objects.all().values()
        return render(request,'addaluno.html',dados)

def tutoria(request):
    dados={}
    dados['professores'] = Professores.objects.all().values()
    return render(request,'tutoria.html',dados)
