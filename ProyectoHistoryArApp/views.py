import traceback
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.middleware.csrf import get_token
import json
import requests
from allauth.socialaccount.models import SocialAccount
from .forms import PuntosInteresForm, RecorridoApiForm, UsuarioForm
from django.core.paginator import Paginator
from urllib3.exceptions import InsecureRequestWarning
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib


BASE_URL = 'https://www.anitmals.com/api/'
"""BASE_URL = 'http://192.168.100.64:8080/api/'"""

def home(request):
    tab = 'home'
    api_url = BASE_URL + 'usuario/'

    response = requests.get(api_url)
    usuarios = response.json()
    imagen_perfil = ''
    if request.user.is_authenticated:
        data = {
            'nombre': request.user.first_name,
            'email': request.user.email,
        } 

        json_data = json.dumps(data)
        csrftoken = get_token(request)

        headers = {
            'X-CSRFToken': csrftoken,
        }
        social = SocialAccount.objects.all()
        for s in social:
            if s.extra_data.get('email') == request.user.email:
                imagen_url = (s.extra_data.get('picture'))
                imagen_response = requests.get(imagen_url)
                imagen_temp_file = open('temp_image.jpg', 'wb')
                imagen_temp_file.write(imagen_response.content)
                imagen_temp_file.close()

        files = {'imagen': open('temp_image.jpg', 'rb')}  

        try:
            response = requests.post(api_url, data=data, headers=headers, files=files)
            response.raise_for_status()  
        except requests.exceptions.RequestException as e:
            print(f'Error en la solicitud POST: {e}')
        
        for s in social:
            if s.extra_data.get('email') == request.user.email:
                imagen_perfil = (s.extra_data.get('picture'))
    return render(request, 'ProyectoHistoryArApp/index.html', {'tab': tab, 'usuarios': usuarios, 'imagen_perfil': imagen_perfil})

def recorrido(request):
    tab = 'recorrido'
    return render(request, 'ProyectoHistoryArApp/recorrido.html', {'tab': tab})

def recorrido_detalle(request):
    tab = 'recorrido'
    return render(request, 'ProyectoHistoryArApp/recorrido_detalle.html', {'tab': tab})

def suscripciones(request):
    tab = 'suscripciones'
    return render(request, 'ProyectoHistoryArApp/suscripciones.html', {'tab': tab})

def panel_admin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("panel_admin")
            else:
                return redirect("panel_admin")
        else:
            return redirect("panel_admin")
    else:
        form = AuthenticationForm()
    return render(request, 'ProyectoHistoryArApp/panel_admin.html', {'form': form})

#Usuarios
@staff_member_required
def usuarios(request):
    api_url = BASE_URL + 'usuario/'
    response = requests.get(api_url)
    usuarios = response.json()
    page = request.GET.get('page', 5)
    buscar = request.GET.get('buscar')
    paginator = Paginator(usuarios, 5)
    usuarios = paginator.get_page(page)
    if buscar is not None and buscar is not "":
        objeto = response.json()
        for usuario in objeto:
            if buscar in usuario['nombre']:
                objeto = [usuario]
        paginator = Paginator(objeto, 5)
        usuarios = paginator.page(page)
        return render(request, 'ProyectoHistoryArApp/usuarios.html', {'usuarios': usuarios, 'paginator': paginator})
    return render(request, 'ProyectoHistoryArApp/usuarios.html', {'usuarios': usuarios, 'paginator': paginator})

@staff_member_required
def crear_usuario(request):
    api_url = BASE_URL + 'usuario/'
    csrftoken = get_token(request)
    headers = {
        'X-CSRFToken': csrftoken,
    }

    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        print(request.FILES)
        print(request.POST)
        if form.is_valid():
            data = {
                'nombre': form.cleaned_data['nombre'],
                'email': form.cleaned_data['email'],
            }

            files = {}
            if request.FILES.get('imagen'):
                imagen_file = request.FILES['imagen']
                files = {'imagen': (imagen_file.name, imagen_file)}

            try:
                response = requests.post(api_url, data=data, headers=headers, files=files)
                response.raise_for_status()
                return redirect('usuarios')
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud POST: {e}')
        else:
            print('entrando por acá', form.errors)
    else:
        form = UsuarioForm()
    return render(request, 'ProyectoHistoryArApp/crear_usuario.html', {'form': form})

@staff_member_required
def editar_usuario(request, id):
    api_url = BASE_URL + 'usuario/' + str(id) + '/'
    csrftoken = get_token(request)
    headers = {
            'X-CSRFToken': csrftoken,
        }
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
            'nombre': form.cleaned_data['nombre'],
            'email': form.cleaned_data['email'],
            }
            files = {}
            if request.FILES.get('imagen'):
                imagen_file = request.FILES['imagen']
                files = {'imagen': (imagen_file.name, imagen_file)}
            try:
                response = requests.put(api_url, data=data, headers=headers, files=files)
                response.raise_for_status()
                return redirect('usuarios')
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud POST: {e}')
        else:
            print(form.errors)
    else:
        response = requests.get(api_url)
        usuario = response.json()
        form = UsuarioForm(usuario)
        editar = True
    return render(request, 'ProyectoHistoryArApp/crear_usuario.html', {'form': form, 'editar': editar})

@staff_member_required
def eliminar_usuario(request, id):
    api_url = BASE_URL + 'usuario/' + str(id) + '/'
    csrftoken = get_token(request)
    headers = {
            'X-CSRFToken': csrftoken,
        }
    try:
        response = requests.delete(api_url, headers=headers)
        response.raise_for_status()
        return redirect('usuarios')
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud DELETE: {e}')
    return render(request, 'ProyectoHistoryArApp/eliminar_usuario.html')

@staff_member_required
def detalle_usuario(request, id):
    api_url = BASE_URL + 'usuario/' + str(id) + '/'
    response = requests.get(api_url)
    usuario = response.json()
    return render(request, 'ProyectoHistoryArApp/detalle_usuario.html', {'usuario': usuario})


#Recorridos
@staff_member_required
def recorridos(request):
    api_url = BASE_URL + 'recorrido/'
    response = requests.get(api_url)
    recorridos = response.json()
    page = request.GET.get('page', 5)
    buscar = request.GET.get('buscar')       
    paginator = Paginator(recorridos, 5)
    recorridos = paginator.get_page(page)
    if buscar is not None and buscar is not "":
        objeto = response.json()
        for recorrido in objeto:
            if buscar in recorrido['nombre']:
                objeto = [recorrido]
        paginator = Paginator(objeto, 1)
        recorridos = paginator.page(page)
        return render(request, 'ProyectoHistoryArApp/recorridos.html', {'recorridos': recorridos, 'paginator': paginator})
    return render(request, 'ProyectoHistoryArApp/recorridos.html', {'recorridos': recorridos, 'paginator': paginator})

@staff_member_required
def editar_recorrido(request, id):
    api_url = BASE_URL + 'recorrido/' + str(id) + '/'
    csrftoken = get_token(request)
    headers = {
            'X-CSRFToken': csrftoken,
        }
    if request.method == 'POST':
        form = RecorridoApiForm(request.POST)
        print(request.POST)
        if form.is_valid():
            data = {
            'nombre': form.cleaned_data['nombre'],
            'descripcion': form.cleaned_data['descripcion'],
            'duracion': form.cleaned_data['duracion'],
            'puntoInteres': form.cleaned_data['puntoInteres'],
            }
        try:
            response = requests.put(api_url, data=data, headers=headers)
            response.raise_for_status()
            return redirect('recorridos')
        except requests.exceptions.RequestException as e:
            print(f'Error en la solicitud POST: {e}')
    else:
        response = requests.get(api_url)
        recorrido = response.json()
        form = RecorridoApiForm(recorrido)
    editar = True
    return render(request, 'ProyectoHistoryArApp/crear_recorrido.html', {'form': form, 'editar': editar})

@staff_member_required
def eliminar_recorrido(request, id):
    api_url = BASE_URL + 'recorrido/' + str(id) + '/'
    csrftoken = get_token(request)
    headers = {
            'X-CSRFToken': csrftoken,
        }
    try:
        response = requests.delete(api_url, headers=headers)
        response.raise_for_status()
        return redirect('recorridos')
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud DELETE: {e}')
    return render(request, 'ProyectoHistoryArApp/eliminar_recorrido.html')

@staff_member_required
def detalle_recorrido(request, id):
    api_url = BASE_URL + 'recorrido/' + str(id) + '/'
    response = requests.get(api_url)
    recorrido = response.json()
    return render(request, 'ProyectoHistoryArApp/detalle_recorrido.html', {'recorrido': recorrido})

@staff_member_required
def crear_recorrido(request):
    api_url = BASE_URL + 'recorrido/'
    csrftoken = get_token(request)
    headers = {
        'X-CSRFToken': csrftoken,
    }

    if request.method == 'POST':
        form = RecorridoApiForm(request.POST)
        if form.is_valid():
            data = {
                'nombre': form.cleaned_data['nombre'],
                'descripcion': form.cleaned_data['descripcion'],
                'duracion': form.cleaned_data['duracion'],
                'puntoInteres': form.cleaned_data['puntoInteres'],
            }

            try:
                response = requests.post(api_url, data=data, headers=headers)
                response.raise_for_status()
                return redirect('recorridos')
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud POST: {e}')
        else:
            print(form.errors)
    else:
        form = RecorridoApiForm()

    return render(request, 'ProyectoHistoryArApp/crear_recorrido.html', {'form': form})

#Puntos de Interes
@staff_member_required
def puntos_interes(request):
    api_url = BASE_URL + 'puntoInteres/'
    response = requests.get(api_url)
    puntos_interes = response.json()
    page = request.GET.get('page', 1)
    buscar = request.GET.get('buscar')       
    paginator = Paginator(puntos_interes, 5)
    puntos_interes = paginator.get_page(page)
    if buscar is not None and buscar is not "":
        objeto = response.json()
        for punto in objeto:
            if buscar in punto['nombre']:
                objeto = [punto]
        paginator = Paginator(objeto, 5)
        puntos_interes = paginator.page(page)
        return render(request, 'ProyectoHistoryArApp/puntos_interes.html', {'puntos_interes': puntos_interes, 'paginator': paginator})
    return render(request, 'ProyectoHistoryArApp/puntos_interes.html', {'puntos_interes': puntos_interes, 'paginator': paginator})

@staff_member_required
def crear_punto_interes(request):
    api_url = BASE_URL + 'puntoInteres/'
    csrftoken = get_token(request)
    headers = {
        'X-CSRFToken': csrftoken,
    }

    if request.method == 'POST':
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        form = PuntosInteresForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                'nombre': form.cleaned_data['nombre'],
                'modelo': form.cleaned_data['modelo'],
                'latitud': form.cleaned_data['latitud'],
                'longitud': form.cleaned_data['longitud'],
            }

            files = {}
            
            if 'imagen' in request.FILES:
                imagen_file = request.FILES['imagen']
                files['imagen'] = (imagen_file.name, imagen_file.read())

            try:
                response = requests.post(api_url, data=data, headers=headers, files=files)
                response.raise_for_status()
                return redirect('puntos_interes')
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud POST: {e}')
        else:
            print(form.errors)
    else:
        form = PuntosInteresForm()

    return render(request, 'ProyectoHistoryArApp/crear_punto_interes.html', {'form': form})


@staff_member_required
def editar_punto_interes(request, id):
    api_url = BASE_URL + 'puntoInteres/' + str(id) + '/'
    csrftoken = get_token(request)
    headers = {
        'X-CSRFToken': csrftoken,
    }

    files = {}

    if request.method == 'POST':
        form = PuntosInteresForm(request.POST, request.FILES) 
        if form.is_valid():
            data = {
                'nombre': form.cleaned_data['nombre'],
                'modelo': form.cleaned_data['modelo'],
                'latitud': form.cleaned_data['latitud'],
                'longitud': form.cleaned_data['longitud'],
            }

            if 'imagen' in request.FILES:
                imagen_file = request.FILES['imagen']
                files['imagen'] = (imagen_file.name, imagen_file.read())

            try:
                response = requests.put(api_url, data=data, files=files, headers=headers)
                response.raise_for_status()
                return redirect('puntos_interes')
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud PUT: {e}')
    else:
        response = requests.get(api_url)
        punto = response.json()
        form = PuntosInteresForm(punto)

    editar = True
    return render(request, 'ProyectoHistoryArApp/crear_punto_interes.html', {'form': form, 'editar': editar})


@staff_member_required
def eliminar_punto_interes(request, id):
    api_url = BASE_URL + 'puntoInteres/' + str(id) + '/'
    csrftoken = get_token(request)
    headers = {
            'X-CSRFToken': csrftoken,
        }
    try:
        response = requests.delete(api_url, headers=headers)
        response.raise_for_status()
        return redirect('puntos_interes')
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud DELETE: {e}')
    return render(request, 'ProyectoHistoryArApp/eliminar_punto_interes.html')

@staff_member_required
def detalle_punto_interes(request, id):
    api_url = BASE_URL + 'puntoInteres/' + str(id) + '/'
    response = requests.get(api_url)
    punto = response.json()
    print(punto)
    return render(request, 'ProyectoHistoryArApp/detalle_punto_interes.html', {'punto': punto})

def generar_compra(request):
    init_point = obtener_init_point()
    return render(request, 'ProyectoHistoryArApp/generar_compra.html', {'init_point': init_point})


def obtener_init_point():
    url = 'https://api.mercadopago.com/checkout/preferences'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.MERCADO_PAGO_ACCESS_TOKEN}'
    }
    data = {
        "items": [
            {
                "title": "Dummy Title",
                "description": "Dummy description",
                "quantity": 1,
                "currency_id": "USD",
                "unit_price": 1
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        init_point = response.json().get('init_point')
        return init_point
    else:
        return None
    

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        # Recibir la notificación de Mercado Pago
        data = json.loads(request.body)
        print("Notificación de Mercado Pago recibida:", data)
        
        # Validar la autenticidad de la notificación
        signature = request.headers.get('x-signature', '')
        if verificar_firma(request.body, signature):
            # Procesar la notificación (actualizar la base de datos, enviar correos electrónicos, etc.)
            # Aquí debes agregar tu lógica para procesar la notificación según tus requerimientos
            
            # Devolver una respuesta HTTP 200 para confirmar la recepción de la notificación
            return HttpResponse(status=200)
        else:
            # La firma no es válida, ignorar la notificación y devolver un error HTTP 400
            return HttpResponse(status=400)
    else:
        # No se permiten solicitudes que no sean POST, devolver un error HTTP 405 
        return HttpResponse(status=405)

def verificar_firma(data, signature):
    # Generar la firma local utilizando la clave secreta de Mercado Pago
    secret = settings.MERCADO_PAGO_WEBHOOK_SECRET
    local_signature = hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()
    
    # Comparar la firma local con la firma recibida
    return hmac.compare_digest(local_signature, signature)








