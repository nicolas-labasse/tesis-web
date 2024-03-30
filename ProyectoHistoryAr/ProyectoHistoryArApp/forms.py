from django import forms
from .models import *
import requests
from django.utils.safestring import mark_safe

BASE_URL = 'https://tesis-web.onrender.com/api/'
"""BASE_URL = 'http://192.168.1.2:8081/api/'"""


class RecorridoApiForm(forms.ModelForm):
    puntoInteres = forms.MultipleChoiceField(
        label='Puntos de Interes', 
        choices=[],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Recorridos
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':'3'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        api_url_puntos = BASE_URL + 'puntoInteres/'
        response = requests.get(api_url_puntos)
        puntos = response.json()

        choices = [(str(punto['id']), str(punto['nombre'])) for punto in puntos]

        self.fields['puntoInteres'].choices = choices

        self.fields['nombre'].label = mark_safe('Nombre <span data-mdb-toggle="tooltip" data-mdb-placement="top" title="se recomienda poner el nombre del primer punto de interes mas el simbolo - y luego el segundo nombre" class="fas fa-exclamation-circle"></span>')


class PuntosInteresForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    modelo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    latitud = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    longitud = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PuntosInteres
        fields = '__all__'

class UsuarioForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    recorridoFavorito = forms.ChoiceField(
        label='Puntos de Interes', 
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})) 
    ultimosRecorridos = forms.ChoiceField(
        label = 'Ultimo Recorrido',
        choices = [],
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        api_url_recorridos = BASE_URL + 'recorrido/'
        response = requests.get(api_url_recorridos)
        recorridos = response.json()

        choices = [(str(recorrido['id']), str(recorrido['nombre'])) for recorrido in recorridos]
        self.fields['recorridoFavorito'].choices = choices

        self.fields['ultimosRecorridos'].choices = choices

class UsuarioPerfilForm(forms.ModelForm):
    nombre = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control custom-field','onchange': 'submitFormNombre();'}))
    
    class Meta:
        model = Usuario
        fields = ['nombre']


class ImagenPerfilForm(forms.Form):
    imagen_update = forms.ImageField()

class ComentariosForm(forms.ModelForm):
    usuario = forms.CharField(widget=forms.HiddenInput(), required=False)
    recorrido = forms.CharField(widget=forms.HiddenInput(), required=False)
    puntuacion = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control','id': 'puntuacion'}))
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'agrega una opinion del recorrido...'}),
        label='Comentario'
    )


    class Meta:
        model = Comentario
        fields = ['puntuacion', 'comentario', 'usuario', 'recorrido']



