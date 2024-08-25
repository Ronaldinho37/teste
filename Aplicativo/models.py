from django.db import models

# Create your models here.

class Alunos(models.Model):
    imagem = models.FileField(upload_to='imagem_alunos', null=True, blank=False)
    serie = models.CharField(max_length=50)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=100)
    #eletiva que ele estuda
    eletiva = models.CharField(max_length=50, null=True, blank=False)

class Professores(models.Model):
    #eletiva que ele ensina
    eletiva = models.CharField(max_length=100,null=True, blank=False)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=100)
    imagem = models.FileField(upload_to='imagem_professores', null=True, blank=False)

class Admins(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=100)
    #retirar o null e o blank daqui
    acoes = models.CharField(max_length=100,null=True, blank=False)
    imagem = models.FileField(upload_to='imagem_admins', null=True, blank=False)

class ImgCarrossel(models.Model):
    img1 = models.FileField(upload_to="img_carrosssel/")
    img2 = models.FileField(upload_to="img_carrosssel/")
    img3 = models.FileField(upload_to="img_carrosssel/")

class Eletivas(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField(max_length=150)
    imagem = models.ImageField(upload_to="img_eletivas/")


class Anuncio(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField(max_length=150)
    imagem = models.ImageField(upload_to="img_anuncio/")

#14 alunos pra cada eletiva
