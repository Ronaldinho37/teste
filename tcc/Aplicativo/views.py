from django.shortcuts import render,redirect,get_object_or_404
from .forms import LoginForm,AddEletivaForm, AnuncioForm, UpdateEletiva
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .models import Alunos,Admins,Professores,ImgCarrossel,Eletivas,Anuncio
from django.contrib import messages
import os
from PIL import Image
#colocar mais de um professor da eletiva
#criar um models para tutores
#esta variável receberá o valor que eu precisarei em todas as funções, ela server para eu não ter que ficar
#repetindo linhas de código. Em quase todas as funções a variável 'dados' hospedará o valor dela.
dados_universsais = {}
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

#dir = Diretório que está localizado a imagem a ser excluída
def excluir_imagem(dir,model):
    #variável que guarda as imagens que estão sendo utilizadas
    imagens_usuarios = []
    #variável que guarda todas imagens da pasta media
    imagens_da_pasta_solicitada = os.listdir(f'{os.getcwd()}/media/{dir}')
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
    for i in imagens_da_pasta_solicitada:
        if i not in imagens_usuarios:
            os.remove(f'{os.getcwd()}/media/{dir}/{i}')
         
   
    return
#funcao que verifica se o usuário da vez pode deletar,cadastrar ou atualizar
def verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,acao):
    #recebe a classificação do user da vez. Classificação: ADMIN, admin, professor ou Aluno
    user = request.session['user']
    #True: sim saia do código e retorne ao index
    #False: não saia pois, o usuário está abilitado a fazer seja lá o que foi requisitado
    #se o usuário não estiver logado retorna True ou seja: o usuário não pode fazer nada pois ainda não está logado
    if user == None:
        return True
    #caso o usuário for um admin tem que ser verificado se ele pode realizar a ação requisitada
    elif user == 'admin':
        #verifica se a ação existe, se existir o fluxo do código não é alterado, se não existir retorna false
        #ou seja: o usuário não pode realizar a ação pois ação não existe
        if request.session.get(f'{acao}') == None:
            return True
        else: 
            return False
    else:
        #se nenhuma dos ifs anteriores der certo então retorne false
        return False
    
def retornar_index(request):
    #if que verifica se o admin já estava logado
    if request.user.is_authenticated:
        request.session['user'] = 'ADMIN'

    dados = {}
    #como a session do Django dura enquanto o navegador estiver aberto(eu abilitei para isso) 
    #quando o usuário abrir o site pela primeira vez vai dar erro, por isso esse try
    #tente pegar essa session, se ela não existir então a crie definindo-a como None ou seja nenhum usuário por enquanto
    try:
        dados['user'] = request.session['user']
    except:
        request.session['user'] = None
        dados['user'] = request.session['user']

    if dados_universsais != dados:
        #caso o usuário for um admin então eu preciso de uma session pra cada ação que ele pode realizar
        #e esse if e for criam elas pra mim
        if dados['user'] == 'admin':
            for i in request.session['lista_de_acoes']:
                dados[f'{i}'] = request.session[f'{i}']
        #atualizando a variável dos dados universsais
        dados_universsais.update(dados)
    
    dados['img_carrossel'] = ImgCarrossel.objects.all()[:1]
    dados['avisos'] = Anuncio.objects.all().order_by("-id")[:3]
    return render(request,'principais/index.html',dados)

def login_viwes(request):
    if request.session['user'] == 'ADMIN':
        return redirect(retornar_index)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data.get('nome')
            password = form.cleaned_data.get('senha')
            if request.session['user'] == 'ADMIN':
                logout(request)
            
            usuario = authenticate(username=nome,password=password)
            if usuario is not None:
                login(request,usuario)
                request.session['user'] = 'ADMIN'
                return redirect(retornar_index)
            
            admins = Admins.objects.all().values()
            for i in admins:
                if i['nome'].lower() == nome and i['senha'] == password:
                    request.session['user'] = 'admin'
                    acoes_lista = i['acoes'].split()
                    request.session['lista_de_acoes'] = acoes_lista
                    for i in acoes_lista:
                        request.session[f'{i}'] = True
                    return redirect(retornar_index)
            #irá checar se o usuário é um professor
            professor = Professores.objects.all().values()
            for i in professor:
                if i['nome'].lower() == nome and i['senha'] == password:
                    request.session['user'] = 'professor'
                    return redirect(retornar_index)
            #irá checar se o usuário é um alunos
            alunos = Alunos.objects.all().values()
            for i in alunos:
                if i['nome'].lower() == nome and i['senha'] == password:
                    request.session['user'] = 'aluno'
                    return redirect(retornar_index)
            messages.info(request,"Usuário ou senha inválidos!")
            dados = {}
            dados['form'] = LoginForm()
            return render(request,'principais/login.html',dados)
    else:
        dados = {}
        dados['form'] = LoginForm()
        return render(request,'principais/login.html',dados)

def eletivas(request):
    dados = dados_universsais.copy()
    dados['pagina'] = "eletivas"
    dados['eletivas'] = Eletivas.objects.all().values()
    dados['user'] = request.session['user']
    return render(request,'eletiva/eletivas.html',dados)

def logout_viwes(request):
    user = request.session['user'] 
    #o admin supremo(ADMIN) é o único que foi criado como um user no django e por isso ele recebe um 
    #tratamento diferente dos demais, a função logout() é própria do Django ela server para deslogar o user
    #que esta logado
    if user == 'ADMIN':
        logout(request)
    #se o usuário for um admin e quer deslogar-se então primeiro eu apago as sessions que comtém os valores 
    #das ações que ele pode realizar 
    elif user == 'admin':
        for i in request.session['lista_de_acoes']:
            del request.session[f'{i}']

        del request.session['lista_de_acoes']

    #por conseguinte eu limpo os valores da variável dos dados universais, pois ela guarda valores referentes
    # ao usuário e já que ele não está mais logado eu não preciso mais delas 
    dados_universsais.clear()
    #definindo o session 'user' como None, desta maneira o código saberá se o usuário está logado ou não
    request.session['user'] = None
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
    #chama a função que verifica se o usuário está apto ou não à adicionar eletivas
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)
    
    if request.method == 'POST':
        #chamando o form 
        form = AddEletivaForm(request.POST, request.FILES)
        if form.is_valid():
            #variável que armazena o nome da eletiva
            eletiva = form.cleaned_data.get('titulo')
            #criando a nova eletiva
            new = Eletivas(titulo=eletiva,descricao=form.cleaned_data.get('descricao'),imagem=form.cleaned_data.get("imagem"))
            #salvando-a
            new.save()
            #redirecionando para a função que adiciona o professor responsável pela eletiva
            return redirect(add_professor)
    else:
        dados = {}
        dados['form'] = AddEletivaForm()
        return render(request,'eletiva/addeletiva.html',dados)

def ver_eletiva(request,eletiva):
    dados = {}
    dados['alunos'] = Alunos.objects.filter(eletiva=eletiva).values()
    try:
        dados['professor'] = Professores.objects.filter(eletiva=eletiva)
    except:
        messages.info(request,'Não professor responsável por essa eletiva')
    if len(dados['alunos']) == 0:
        messages.info(request,'Não há alunos nesta eletiva')
    return  render(request,'eletiva/eletiva.html',dados)
    

def add_professor(request):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        eletiva = request.POST.get('eletiva')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        imagem = request.FILES.get('imagem')
        form = [nome,eletiva,email,senha]
        for i in form:
            if i == '':
                dados = {}
                dados['eletivas'] = Eletivas.objects.all().values()
                messages.info(request,'Nenhum campo pode ser deixado em branco exceto o de imagem')
                return render(request,'addprofessor.html',dados)
        professor = Professores(eletiva=eletiva,nome=nome,email=email,senha=senha,imagem=imagem)
        professor.save()
        return redirect(eletivas)
    else:
        dados={}
        dados['eletivas'] = Eletivas.objects.all().values()
        return render(request,'professor/addprofessor.html',dados)

def add_aluno(request):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)
    else:
        if request.method == 'POST':
            serie=request.POST.get('serie')
            nome=request.POST.get('nome')
            email=request.POST.get('email')
            senha=request.POST.get('senha')
            eletiva=request.POST.get('select')

            campos = [serie,nome,email,senha,eletiva]
            for i in campos:
                if i == '':
                    dados={}
                    dados['eletivas'] = Eletivas.objects.all().values()
                    messages.info(request,'A imagem de perfil é opcional porém os outros campos são obrigatórios')
                
                    return render(request,'aluno/addaluno.html',dados)
            aluno = Alunos(imagem=request.FILES.get('imagem'),serie=serie,nome=nome,email=email,senha=senha,eletiva=eletiva)
            aluno.save()
            return redirect(ver_eletiva,eletiva=request.POST.get('select'))
        else:
            dados={}
            dados['eletivas'] = Eletivas.objects.all().values()
            messages.info(request,'A imagem de perfil é opcional')
            return render(request,'aluno/addaluno.html',dados)

def tutoria(request):
    dados=dados_universsais.copy()
    dados['pagina'] = 'tutoria'
    dados['professores'] = Professores.objects.all().values()
    return render(request,'principais/tutoria.html',dados)


def addanuncio(request):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)
    else:
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
        if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'deletar') == True:
            return redirect(retornar_index)
        anuncio = Anuncio.objects.get(id=anuncio_id)
        if request.method == 'POST':
            sim = request.POST.get('sim')
            if sim == 'on':
                anuncio.delete()
            return redirect(retornar_index)
        else:
            return render (request, 'anuncio/deletaranuncio.html')

def update_eletiva(request,id):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'atualizar') == True:
        return redirect(retornar_index)
    else:
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
            dados = dados_universsais.copy()
            dados['eletiva'] = Eletivas.objects.values().get(id=id)
            dados['modo'] = "update"
            dados['form'] = UpdateEletiva(instance=eletiva)
            return render(request,'eletiva/addeletiva.html',dados)

def sobre(request):
    dados = dados_universsais.copy()
    dados['pagina'] = 'sobre'
    return render(request,'principais/about.html',dados)

def deletar(request,user): 
        if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'deletar') == True:
            return redirect(retornar_index)
        dados = {}
        dados['user'] = user
        dados['modo'] = 'deletar'
        if user.lower() == 'aluno':
            dados['usuarios'] = Alunos.objects.all().values()
            return render(request,'deletar/deletar.html', dados)
        elif user.lower() == 'professor':
            dados['usuarios'] = Professores.objects.all().values()
            return render(request,'deletar/deletar.html', dados)
        elif user.lower() == 'admin':
            dados['usuarios'] = Admins.objects.all().values()
            return render(request,'deletar/deletar.html', dados)
        else:
            messages.info(request,'Usuário não identificado')
            return redirect(retornar_index)

        
def deletar_com_ids(request,user,id):
        if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'deletar') == True:
            return redirect(retornar_index)
    
        dados = {}
        dados['lista_id'] = id.split(',')
        dados['tam_lista_id'] = len(dados['lista_id'])
        if request.method == 'POST':
            sim = request.POST.get('sim')
            nao = request.POST.get('nao')
            if sim == 'on' and nao != 'on':
                if user == "aluno":
                    for i in dados['lista_id']:
                        Alunos.objects.get(id=i).delete()

                    messages.info(request,f'Todo(s) o(s) {dados["tam_lista_id"]} aluno(s) deletado(s)')
                    return redirect(deletar,user=user)
                elif user == "admin":
                    for i in dados['lista_id']:
                        Admins.objects.get(id=i).delete()

                    messages.info(request,f'Todo(s) o(s) {dados["tam_lista_id"]} admin(s) deletado(s)')
                    return redirect(deletar,user=user)
                elif user == "admin":
                    for i in dados['lista_id']:
                        Professores.objects.get(id=i).delete()

                    messages.info(request,f'Todo(s) o(s) {dados["tam_lista_id"]} professores(s) deletado(s)')
                    return redirect(deletar,user=user)
            
            elif nao != "on" and sim != "on":
                messages.info(request,"selecione um dos valores")
                return redirect(deletar_com_ids, user=user,id=id)
            else:
                return redirect(deletar,user=user)
        else:
            return render(request,'deletar/deletar_com_ids.html',dados)

def add_admin(request):
    if verificar_se_o_usuario_pode_realizar_a_acao_equisitada(request,'cadastrar') == True:
        return redirect(retornar_index)
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        imagem = request.FILES.get('imagem')
        #checkboxes
        checkboxes = ['deletar','atualizar','cadastrar']
        acoes_permitidas = ""
        for i in checkboxes:
            checkbox = request.POST.get(i)
            if checkbox == 'on':
                acoes_permitidas += f' {i}'
        novo_adm = Admins(nome=nome,senha=senha,email=email,acoes=acoes_permitidas,imagem=imagem)
        novo_adm.save()
        return redirect(retornar_index)
    else:
        return render(request,'acoes_principais/template_add.html')
    
def update(request,user):
    dados = {}
    dados['user'] = user
    if user.lower() == 'aluno':
        dados['usuarios'] = Alunos.objects.all().values()
        return render(request,'update/update.html', dados)
    elif user.lower() == 'professor':
        dados['usuarios'] = Professores.objects.all().values()
        return render(request,'update/update.html', dados)
    elif user.lower() == 'admin':
        dados['usuarios'] = Admins.objects.all().values()
        return render(request,'update/update.html', dados)
    else:
        messages.info(request,'Usuário não identificado')
        return redirect(retornar_index)

def update_com_id(request,user,id):
    tabela_do_user = []
    
    if user == 'aluno':
        tabela_do_user.append(Alunos)
    elif user == 'professores':
        tabela_do_user.append(Professores)
    elif user == 'admin':
        tabela_do_user.append(Admins)
   
    user_a_ser_atualizado = tabela_do_user[0].objects.get(id=id)
    print(user_a_ser_atualizado)
    
    campos_atigos_do_user = [user_a_ser_atualizado.nome,user_a_ser_atualizado.email,user_a_ser_atualizado.senha,user_a_ser_atualizado.imagem,user_a_ser_atualizado.eletiva,user_a_ser_atualizado.serie]

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        imagem = request.FILES.get('imagem')
        eletiva = request.POST.get('eletiva')
        serie = request.POST.get('serie')
        print(user_a_ser_atualizado.imagem)

        campos = [nome,email,senha,imagem,eletiva,serie]
        

        tam = 0
        for i in campos:
            if i != campos_atigos_do_user[0]:
                if tam == 0:
                    user_a_ser_atualizado.nome = i
                elif tam == 1:
                    user_a_ser_atualizado.email = i
                elif tam == 2:
                    user_a_ser_atualizado.senha = i
                elif tam == 3 and imagem != None:
                    user_a_ser_atualizado.imagem = i
                elif tam == 4:
                    user_a_ser_atualizado.eletiva = i
                elif tam == 5:
                    user_a_ser_atualizado.serie = i
            tam += 1
        user_a_ser_atualizado.save()
        return redirect(update,user=user)

        


    else:
        dados = {}
        dados['tabela'] = tabela_do_user[0].objects.get(id=id)
        dados['eletivas'] = Eletivas.objects.all().values()
        dados['user'] = user
        return render(request, 'update/update_com_id.html', dados)


