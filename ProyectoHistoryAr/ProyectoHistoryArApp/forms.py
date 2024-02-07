from django import forms
from .models import *
import requests

BASE_URL = 'https://www.anitmals.com/api/'
"""BASE_URL = 'http://192.168.100.64:8080/api/'"""


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

        choices = [(str(punto['id']), str(punto['id'])) for punto in puntos]

        self.fields['puntoInteres'].choices = choices


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
    recorridoFavorito = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    ultimosRecorridos = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = '__all__'



