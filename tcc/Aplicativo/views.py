from django.shortcuts import render,redirect,get_object_or_404
from .forms import LoginForm,AddEletivaForm, AnuncioForm, UpdateEletiva
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .models import Alunos,Admins,Professores,ImgCarrossel,Eletivas,Anuncio
from django.contrib import messages
import os
from PIL import Image
# roni
# r@ni
# ImgCarrossel.objects.all().delete()
#1920 x 695 
# Create your views here.

#como codificar palavras
# import rsa
# (publickey, privatekey) = rsa.newkeys(100)
# m = "oi".encode('utf8')
# ciphertext = rsa.encrypt(m, publickey)
# m2 = rsa.decrypt(ciphertext, privatekey)
# print(ciphertext)
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
    #if que verifica se o admin já estava logado
    if request.user.is_authenticated:
        user.clear()
        user.append('admin')

    dados = {}
    dados['user'] = user[0]
    dados['img_carrossel'] = ImgCarrossel.objects.all()[:1]
    dados['avisos'] = Anuncio.objects.all().order_by("-id")[:3]
    return render(request,'principais/index.html',dados)

def login_viwes(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(user[0])
            if user[0] == 'admin':
                logout(request)
            
            usuario = authenticate(username=form.cleaned_data.get('nome'),password=form.cleaned_data.get('senha'))
            if usuario is not None:
                login(request,usuario)
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
        return render(request,'principais/login.html',dados)

def eletivas(request):
    dados = {}
    dados['pagina'] = "eletivas"
    dados['eletivas'] = Eletivas.objects.all().values()
    dados['user'] = user[0]
    return render(request,'eletiva/eletivas.html',dados)

def logout_viwes(request):
    if user[0] == 'admin':
        logout(request)
    user.clear()
    user.append(None)
    return redirect(retornar_index)

def definir_carrossel(request):
    if request.method == 'POST':
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        #colocando os arquivos em uma lista, assim posso percorrer seu valores
        imagens = [img1,img2,img3]
        #variável que irá armazenar as imagens finais
        imagens_finais = []
        #pegando as imagens da pasta img_carrosssel
        diretorio_carrossel = os.listdir(f'{os.getcwd()}/media/img_carrosssel')
        #deletando os valores velhos
        ImgCarrossel.objects.all().delete()
        #percorre as imagens do form
        for img in imagens:
            #imagem da vez
            imagem_inserida = Image.open(img)
            #byte da imagem da vez
            imagem_inserida_bytes = imagem_inserida.tobytes("xbm", "rgb")
            tam = 0
            #percorre os valores da  pasta img_carrosssel
            for i in diretorio_carrossel:
                tam += 1
                #transforma o arquivo da pasta em bytes
                img_do_diretorio = Image.open(f'{os.getcwd()}/media/img_carrosssel/{i}').tobytes("xbm", "rgb")
                #se a imagem já foi adicionada adicionará seu respectivo caminho
                if imagem_inserida_bytes == img_do_diretorio or img in imagens_finais:
                    imagens_finais.append(f'img_carrosssel/{i}')
                    break
                #se a imagem não foi adicionada e o loop não quebrou então adicionará uma imagem 
                if tam == len(diretorio_carrossel):
                    imagens_finais.append(img)
                    break
        '''variável que armazena as imagens da variavel "imagens_finais". Essas imagens passarão por uma consulta
        para que seja sertificado que ambas não são iguai'''
        verificacao = []
        verificacao_bytes = []
        #esse loop adiciona somente as imagens na variavel "verificacao"
        for i in imagens_finais:
            if str(type(i)) != "<class 'str'>":
                verificacao.append([i,imagens_finais.index(i)])
        #esse loop passará para a variável "imagen_finais" a imagem se ela não existir e se ela existir então passará seu respectivo caminho
        for i in verificacao:
           #para ter com quem comparar essa variável armazenará os outros valores da lista verificacao
           verificacao_bytes = imagens_finais.copy()
           verificacao_bytes.remove(i[0])
           for e in verificacao_bytes:
               #se não for uma string como no caso do caminho da imagem
               if str(type(e)) != "<class 'str'>":
                   #consegui diferenciar as imagens somente passando-as para bytes
                   if Image.open(i[0]).tobytes("xbm","rgb") == Image.open(e).tobytes("xbm","rgb"):
                       #remove o antigo valor
                       imagens_finais.pop(i[1])
                       #e coloca um caminho no lugar da imagen coso ela já exista
                       imagens_finais.insert(i[1],f"img_carrosssel/{Image.open(e).fp}".replace(" ","_"))
        print(imagens_finais)
        carrossel = ImgCarrossel(img1=imagens_finais[0],img2=imagens_finais[1],img3=imagens_finais[2])
        carrossel.save()
        model = ImgCarrossel.objects.all().values()
        excluir_imagem("img_carrosssel",model)

        return redirect(retornar_index)
    else:
        return render(request,'principais/imgcarrossel.html')

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
        return render(request,'eletiva/addeletiva.html',dados)

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
        return  render(request,'eletiva/eletiva.html',dados)
    elif pode_ir[0] == False and pode_ir[1] == True:
        messages.info(request,'Nenhum aluno nesta eletiva')
        dados['professor'] = Professores.objects.get(eletiva=eletiva)
        return  render(request,'eletiva/eletiva.html',dados)
    elif pode_ir[0] == True and pode_ir[1] == False:
        messages.info(request,'Nenhum professor nesta eletiva')
        dados['alunos'] = Alunos.objects.all().filter(eletiva=eletiva)
        return  render(request,'eletiva/eletiva.html',dados)
    else:
        messages.info(request,'Nenhum aluno e professor nesta eletiva')
        return  render(request,'eletiva/eletiva.html',dados)
    

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
        return render(request,'professor/addprofessor.html',dados)

def add_aluno(request):
    if request.method == 'POST':
        aluno = Alunos(serie=request.POST.get('serie'),nome=request.POST.get('nome'),email=request.POST.get('email'),senha=request.POST.get('senha'),eletiva=request.POST.get('select'))
        aluno.save()
        return redirect(ver_eletiva,eletiva=request.POST.get('select'))
    else:
        dados={}
        dados['eletivas'] = Eletivas.objects.all().values()
        return render(request,'aluno/addaluno.html',dados)

def tutoria(request):
    dados={}
    dados['user'] = user[0]
    dados['pagina'] = 'tutoria'
    dados['professores'] = Professores.objects.all().values()
    return render(request,'principais/tutoria.html',dados)


def addanuncio(request):
    if request.method == 'POST':
        form = AnuncioForm(request.POST, request.FILES)
        if form.is_valid():
            anuncio = Anuncio(titulo=form.cleaned_data.get('titulo'),descricao=form.cleaned_data.get('descricao'),imagem=form.cleaned_data.get("imagem"))
            anuncio.save()
            return redirect(retornar_index)
        
    else:
        form = AnuncioForm()
        return render(request, 'anuncio/addanuncio.html', {'form': form})
    

def deletar_anuncio(request, anuncio_id):
    anuncio = Anuncio.objects.get(id=anuncio_id)
    if request.method == 'POST':
        sim = request.POST.get('sim')
        if sim == 'on':
            anuncio.delete()
        return redirect(retornar_index)
    else:
        return render (request, 'anuncio/deletaranuncio.html')

def update_eletiva(request,id):
    eletiva = get_object_or_404(Eletivas, id=id)
    eletiva_1 = str(eletiva.titulo)
    
    if request.method == 'POST':
        form = UpdateEletiva(request.POST,request.FILES,instance=eletiva)
        if form.is_valid():
            if form.cleaned_data.get('titulo') != eletiva_1:
                professores = Professores.objects.filter(eletiva=eletiva_1)
                alunos = Alunos.objects.filter(eletiva=eletiva_1)
                if len(professores) != 0:
    
                    prof_atualizar = Professores.objects.get(eletiva=eletiva_1)
                    prof_atualizar.eletiva = form.cleaned_data.get('titulo')
                    prof_atualizar.save()
                if len(alunos) != 0:
                    alunos = Alunos.objects.filter(eletiva=eletiva_1)
                    for aluno in alunos:
                        aluno.eletiva = form.cleaned_data.get('titulo')
                        aluno.save()
    
            form.save()
            return redirect(eletivas)
        else:
            dados = {}
            dados['eletiva'] = Eletivas.objects.values().get(id=id)
            dados['modo'] = "update"
            messages.info(request,'Dados inválidos')
            return render(request,'eletiva/addeletiva.html',dados)
    else:
        dados = {}
        dados['user'] = user[0]
        dados['eletiva'] = Eletivas.objects.values().get(id=id)
        dados['modo'] = "update"
        dados['form'] = UpdateEletiva(instance=eletiva)
        return render(request,'eletiva/addeletiva.html',dados)

def sobre(request):
    dados = {}
    dados['user'] = user[0]
    dados['pagina'] = 'sobre'
    return render(request,'principais/about.html',dados)

