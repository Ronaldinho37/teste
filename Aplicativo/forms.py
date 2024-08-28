from django import forms
from .models import Eletivas, Anuncio

class LoginForm(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(attrs={'name':'nome'}),label="Nome Completo")
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'name':'senha'}))

class AddEletivaForm(forms.Form):
    titulo = forms.CharField(max_length=50)
    descricao = forms.CharField(widget=forms.Textarea(attrs={'name':'descricao'}), max_length=150)
    imagem = forms.ImageField(widget=forms.FileInput(attrs={'name':'imagem'}))
    link = forms.URLField(widget=forms.URLInput(attrs={'name':'link'}), max_length=150)

class AnuncioForm(forms.Form):
    titulo = forms.CharField(max_length=100)
    descricao = forms.CharField(widget=forms.Textarea(attrs={'name':'descricao'}), max_length=400)
    imagem = forms.ImageField(widget=forms.FileInput(attrs={'name':'imagem'}))
    link = forms.URLField(widget=forms.URLInput(attrs={'name':'link'}), max_length=150)
    

class UpdateEletiva(forms.ModelForm):
    class Meta:
        model = Eletivas
        fields = ['titulo', 'descricao', 'imagem']
# class DefinirCarrossel(forms.Form):
#     img1 = forms.ImageField(widget=forms.FileInput(attrs={'class':"form-control",'id':"inputGroupFile01",'name':"imdeded",'onchange':"previewImage(event, 'preview1')"}))
    

   

    