from django.urls import reverse
import math
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
import json
import requests
from allauth.socialaccount.models import SocialAccount
from .forms import ImagenPerfilForm, PuntosInteresForm, RecorridoApiForm, UsuarioForm, ComentariosForm, UsuarioPerfilForm
from django.core.paginator import Paginator
from urllib3.exceptions import InsecureRequestWarning
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import hmac
import hashlib
import datetime
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

"""BASE_URL = 'https://tesis-web.onrender.com/api/'"""
BASE_URL = 'http://192.168.1.2:8081/api/'

def contacto(request):
    tab = "#contacto"
    return redirect('/'+tab)
    
def home(request):
    tab = 'home'
    texto_sm = "Descubre la Historia a Través de tus Ojos\nBienvenido a Historyar, la aplicación de realidad aumentada que te llevará en un viaje único a través del tiempo mientras caminas por lugares históricos. Imagina poder presenciar momentos clave de la historia de una manera completamente nueva: viendo cómo cobran vida justo frente a ti mientras exploras el mundo que te rodea.\nNuestra innovadora tecnología de realidad aumentada te permite fusionar el pasado con el presente de una manera cautivadora. Desde las grandiosas batallas que moldearon naciones hasta los momentos íntimos que transformaron vidas, Historyar te sumerge en una experiencia inmersiva que trasciende las páginas de los libros de historia."
    texto_intro ="Bienvenido a Historyar, la aplicación de realidad aumentada que te llevará en un viaje único a través del tiempo mientras caminas por lugares históricos. Imagina poder presenciar momentos clave de la historia de una manera completamente nueva: viendo cómo cobran vida justo frente a ti mientras exploras el mundo que te rodea.\nNuestra innovadora tecnología de realidad aumentada te permite fusionar el pasado con el presente de una manera cautivadora. Desde las grandiosas batallas que moldearon naciones hasta los momentos íntimos que transformaron vidas, Historyar te sumerge en una experiencia inmersiva que trasciende las páginas de los libros de historia."

    #Usuarios
    api_url = BASE_URL + 'usuario/' + 'usuarios/'
    response = requests.get(api_url)
    usuarios = response.json()

    usuario_registrado = False
    usuario_inactivo = False

    if request.user.is_authenticated:
        for usuario in usuarios:
            if request.user.email == usuario['email']:
                usuario_registrado = True
                break
            else:
                usuario_registrado = False

    if usuario_registrado == False:
        if request.user.is_authenticated:

            data = {
                'nombre': request.user.username,
                'email': request.user.email,
                'activo': True,
            } 

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
                response = requests.post(api_url, data=data, files=files, headers=headers)
                response.raise_for_status()  
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud POST: {e}')
    if request.user.is_authenticated:
        for usuario in usuarios:
            if request.user.email == usuario['email']:
                if usuario['activo'] == False:
                    usuario_inactivo = True
                    logout(request)
                    messages.error(request, 'Usuario inactivo, por favor contacte al administrador.')

    return render(request, 'ProyectoHistoryArApp/index.html', {'tab': tab, 'usuarios': usuarios, 'texto_intro': texto_intro, 'texto_sm': texto_sm, 'usuario_inactivo': usuario_inactivo})

def recorrido(request):
        tab = 'recorrido'
        #Recorridos
        recorridos = get_json('recorrido/recorrido/')

        buscar = request.GET.get('buscar')      

        nombres1 = []
        nombres2 = []
        
        for r in recorridos:
            nombre_completo = r['nombre']
            partes_nombre = nombre_completo.split('-')
            if len(partes_nombre) == 2:
                nombres1.append(partes_nombre[0].strip())
                nombres2.append(partes_nombre[1].strip())
            elif len(partes_nombre) == 1:
                nombres1.append(partes_nombre[0].strip())
                nombres2.append('')
            else:
                print(f"Error: Nombre no válido: {nombre_completo}")

        if buscar is not None and buscar is not "":
            tab = 'buscar'
            objeto = recorridos.json()
            resultados = []
            for recorrido in objeto:
                if buscar.lower() in recorrido['nombre'].lower():
                    resultados.append(recorrido)
            return render(request, 'ProyectoHistoryArApp/recorrido.html', {'tab': tab,'resultados': resultados, 'nombres1': nombres1, 'nombres2': nombres2})
        
        
        usuario = get_json('usuario/usuarios/')
        favoritos = []
        try:
            for u in usuario:
                if u['email'] == request.user.email:
                    favoritos = u['recorridoFavorito']
        except:
            favoritos = []
        
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect("recorrido")
                else:
                    return redirect("recorrido")
            else:
                return redirect("recorrido")
        else:
            form = AuthenticationForm()

        return render(request, 'ProyectoHistoryArApp/recorrido.html', {'tab': tab, 'recorridos': recorridos, 'nombres1': nombres1, 'nombres2': nombres2, 'favoritos': favoritos, 'form': form})

def recorrido_detalle(request, id):
    tab = 'recorrido'
    recorrido = get_json('recorrido/recorrido/' + str(id) + '/')
    api_url = BASE_URL + 'calificacion/'
    response_comentario = requests.get(api_url)
    comentarios = response_comentario.json()
    comentario_json = json.dumps(comentarios)
    
    if request.user.is_authenticated:
        form = ComentariosForm()
    else:
        form = AuthenticationForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentariosForm(request.POST)
            if form.is_valid():
                data = {
                    'usuario': str(request.user.id),
                    'recorrido': str(recorrido['id']),
                    'comentario': form.cleaned_data['comentario'],
                    'puntuacion': form.cleaned_data['puntuacion'],
                }
                csrftoken = get_token(request)
                headers = {
                    'X-CSRFToken': csrftoken,
                }
                try:
                    response = requests.post(api_url, data=data, headers=headers)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f'Error en la solicitud POST: {e}')
                return redirect('recorrido_detalle', id=id)
        else:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("recorrido_detalle", id=id)
    else:
        comentario_existente = None
        for comentario in comentarios:
            if request.user.id == comentario['usuario'] and recorrido['id'] == comentario['recorrido']:
                comentario_existente = comentario
                break

        if request.user.is_authenticated and comentario_existente:
            initial_data = {
                'usuario': request.user.id,
                'recorrido': recorrido['id'],
                'puntuacion': comentario_existente['puntuacion'],
                'comentario': comentario_existente['comentario'],
            }
            form = ComentariosForm(initial=initial_data)
        elif request.user.is_authenticated:
            initial_data = {
                'usuario': request.user.id,
                'recorrido': recorrido['id'],
                'puntuacion': '',
                'comentario': '',
            }
            form = ComentariosForm(initial=initial_data)

    calificaciones = []
    usuarios = []
    puntuacion = 0
    cantidad_calificaciones = 0
    puntuacion_total = 0
    for comentario in comentarios:
        if comentario['recorrido'] == recorrido['id']:
            calificaciones.append(comentario)
            puntuacion_total += comentario['puntuacion']
            cantidad_calificaciones += 1
            api_url_user = BASE_URL + 'usuario/' + 'usuarios/' + str(comentario['usuario']) + '/'
            response_user = requests.get(api_url_user)
            usuarios.append(response_user.json())

    if cantidad_calificaciones > 0:
        puntuacion = math.ceil((puntuacion_total / (cantidad_calificaciones * 5)) * 5)
    else:
        puntuacion = 0

    for calificacion in calificaciones:
        calificacion['stars_range'] = range(calificacion['puntuacion'])

    return render(request, 'ProyectoHistoryArApp/recorrido_detalle.html', {
        'tab': tab,
        'form': form,
        'recorrido': recorrido,
        'calificaciones': calificaciones,
        'usuarios': usuarios,
        'puntuacion': puntuacion,
        'comentario_json': comentario_json
    })

@login_required
def suscripciones(request):
    api_url = BASE_URL + 'transaccion/'
    response = requests.get(api_url)
    transacciones = response.json()
    transacciones_usuario = []
    fecha_expiracion = []
    suscripcione_valida = False
    fecha_expiracion_str = ''
    terminos_condiciones = 'La Suscripción Mensual de Recorridos Turísticos Ilimitados te ofrece acceso exclusivo a una amplia gama de recorridos turísticos durante un mes completo. Con esta suscripción, podrás explorar destinos turísticos emocionantes y descubrir lugares de interés histórico, cultural y natural sin restricciones. Además, podrás disfrutar de recorridos turísticos ilimitados en cualquier momento y lugar, lo que te permitirá planificar tus viajes de manera flexible y conveniente. Con la Suscripción Mensual de Recorridos Turísticos Ilimitados, podrás disfrutar de una experiencia de viaje única y memorable que te permitirá descubrir el mundo de una manera nueva y emocionante.'
    for t in transacciones:
        if t['usuario'] == request.user.id:
            fecha_creacion = datetime.datetime.strptime(t['fechaCreacion'], '%Y-%m-%d')
            fecha_exp = fecha_creacion + datetime.timedelta(days=30)
            if fecha_exp > datetime.datetime.now():
                suscripcione_valida = True
                fecha_expiracion.append(fecha_exp)
                transacciones_usuario.append(t)

    if fecha_expiracion:
        fecha_expiracion_str = max(fecha_expiracion).strftime('%d/%m/%Y')
    init_point = obtener_init_point(request)
    return render(request, 'ProyectoHistoryArApp/suscripcion.html', {'transacciones': transacciones_usuario, 'fecha_expiracion': fecha_expiracion_str, 'suscripcione_valida': suscripcione_valida, 'terminos_condiciones': terminos_condiciones, 'init_point': init_point})

def suscribirse(request):
    if request.method == 'POST':
        formLogin = AuthenticationForm(request, data=request.POST)
        if formLogin.is_valid():
            username = formLogin.cleaned_data.get('username')
            password = formLogin.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("suscribirse")
            else:
                return redirect("suscribirse")
        else:
            return redirect("suscribirse")
    else:
        formLogin = AuthenticationForm()
    tab = 'suscribirse'
    card_1 = 'Te invitamos a un emocionante viaje a través de la historia en realidad aumentada. Descubre puntos de interés histórico en la ciudad mientras exploras con tu dispositivo móvil. Desde monumentos emblemáticos hasta lugares ocultos, cada rincón cobra vida con detalles históricos fascinantes.'
    card_2 = 'Disfruta de la libertad de elegir. Tu suscripción está activa durante el mes que elijas y te permite sumergirte en la historia a tu manera. Si deseas continuar tu aventura histórica el próximo mes, la renovación es sencilla y sin complicaciones.'
    card_3 = 'Sumérgete en una amplia gama de puntos de interés histórico. Desde encantadores rincones antiguos hasta hitos monumentales, experimentarás la evolución de la ciudad a lo largo del tiempo.'
    init_point = obtener_init_point(request)
    return render(request, 'ProyectoHistoryArApp/suscripciones.html', {'tab': tab, 'card_1': card_1, 'card_2': card_2, 'card_3': card_3, 'init_point': init_point, 'formLogin': formLogin})

def panel_admin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password, is_staff=True)

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
    #Usuarios
    usuarios = get_json('usuario/usuarios/')

    #Recorridos
    recorridos = get_json('recorrido/')

    #Filtros
    page = request.GET.get('page', 5)
    buscar = request.GET.get('buscar')
    paginator = Paginator(usuarios, 5)
    usuarios = paginator.get_page(page)
    recorrido = ''
    if recorridos:
        for usuario in usuarios:
            if usuario['recorridoFavorito'] is not None:
                api_recorrido = BASE_URL + 'recorrido/' + str(usuario['recorridoFavorito']) + '/'
                response_recorrido = requests.get(api_recorrido)
                if response_recorrido.status_code == 200:  
                    recorrido = response_recorrido.json()
                    usuario['recorridoFavorito'] = recorrido['nombre']
                        
        
        for usuario in usuarios:
            for recorrido in recorridos:
                if usuario['ultimosRecorridos'] == recorrido['id']:
                    usuario['ultimosRecorridos'] = recorrido['nombre']
            if usuario['ultimosRecorridos'] is None:
                usuario['ultimosRecorridos'] = ''
    
    if buscar is not None and buscar.strip():
        resultados = [usuario for usuario in usuarios if buscar.lower() in usuario['nombre'].lower() or buscar.lower() in usuario['email'].lower()]
        paginator = Paginator(resultados, 5)
        usuarios = paginator.get_page(page)
        return render(request, 'ProyectoHistoryArApp/usuarios.html', {'usuarios': usuarios, 'paginator': paginator})
    usuarios = paginator.get_page(page)
    return render(request, 'ProyectoHistoryArApp/usuarios.html', {'usuarios': usuarios, 'paginator': paginator, 'recorrido': recorrido})

@staff_member_required
def crear_usuario(request):
    api_url = BASE_URL + 'usuario/' + 'usuarios/'
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
                'recorridoFavorito': form.cleaned_data['recorridoFavorito'],
                'ultimosRecorridos' : form.cleaned_data['ultimosRecorridos'],
                'activo': True,
            }

            files = {}
            if request.FILES.get('imagen'):
                imagen_file = request.FILES['imagen']
                files = {'imagen': (imagen_file.name, imagen_file)}

            try:
                response = requests.post(api_url, data=data, headers=headers, files=files)
                response.raise_for_status()
                messages.success(request, 'Usuario creado correctamente.')
                return redirect('usuarios')
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud POST: {e}')
                messages.error(request, 'Error en la creación del usuario, por favor intente nuevamente.')
                return redirect('crear_usuario')
        else:
            print(form.errors)
            messages.error(request, 'Error en la creación del usuario, revise los campos ingresados en el formulario.')
    else:
        form = UsuarioForm()
    return render(request, 'ProyectoHistoryArApp/crear_usuario.html', {'form': form})

@staff_member_required
def editar_usuario(request, id):
    api_url = BASE_URL + 'usuario/' + 'usuarios/' + str(id) + '/'
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
            'recorridoFavorito': form.cleaned_data['recorridoFavorito'],
            'ultimosRecorridos' : form.cleaned_data['ultimosRecorridos'],
            }
            files = {}
            if request.FILES.get('imagen'):
                imagen_file = request.FILES['imagen']
                files = {'imagen': (imagen_file.name, imagen_file)}
            try:
                response = requests.put(api_url, data=data, headers=headers, files=files)
                response.raise_for_status()
                messages.success(request, 'Usuario editado correctamente.')
                return redirect('usuarios')
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud POST: {e}')
                messages.error(request, 'Error en la edición del usuario, por favor intente nuevamente.')
                return redirect('usuarios')
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
    api_url = BASE_URL + 'usuario/' + 'estado_usuario/' + str(id) + '/'
    csrftoken = get_token(request)
    headers = {
            'X-CSRFToken': csrftoken,
        }
    try:
        response = requests.put(api_url, headers=headers)
        response.raise_for_status()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('usuarios')
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud DELETE: {e}')
        messages.error(request, 'Error en la eliminación del usuario, por favor intente nuevamente.')
        return redirect('usuarios')

@staff_member_required
def detalle_usuario(request, id):
    usuario = get_json('usuario/usuarios/' + str(id) + '/')
    
    #Recorridos
    recorridos = get_json('recorrido/')

    recorrido = ''
    for recorrido in recorridos:
        if usuario['ultimosRecorridos'] == recorrido['id']:
            usuario['ultimosRecorridos'] = recorrido['nombre']

    if usuario['recorridoFavorito'] is not None:
        api_recorrido = BASE_URL + 'recorrido/' + str(usuario['recorridoFavorito']) + '/'
        response_recorrido = requests.get(api_recorrido)
            
        if response_recorrido.status_code == 200:  
            recorrido = response_recorrido.json()
            usuario['recorridoFavorito'] = recorrido['nombre']

    return render(request, 'ProyectoHistoryArApp/detalle_usuario.html', {'usuario': usuario, 'recorrido': recorrido})

#Recorridos
@staff_member_required
def recorridos(request):
    #Recorridos
    recorridos = get_json('recorrido/recorrido/')
    puntos_activos = 0
    for recorrido in recorridos:
        for punto in recorrido['puntoInteres']:
            if punto['activo'] == True:
                puntos_activos += 1
        if puntos_activos == 0 and recorrido['activo'] == True:
            eliminar_recorrido(request,recorrido['id'])

    page = request.GET.get('page', 5)
    buscar = request.GET.get('buscar')       
    paginator = Paginator(recorridos, 5)
    recorridos = paginator.get_page(page)
    
    if buscar is not None and buscar.strip():
        resultados = [recorrido for recorrido in recorridos if buscar.lower() in recorrido['nombre'].lower()]
        paginator = Paginator(resultados, 5)
        recorridos = paginator.get_page(page)
        return render(request, 'ProyectoHistoryArApp/recorridos.html', {'recorridos': recorridos, 'paginator': paginator})
    
    recorridos = paginator.get_page(page)
    
    return render(request, 'ProyectoHistoryArApp/recorridos.html', {'recorridos': recorridos, 'paginator': paginator})

@staff_member_required
def editar_recorrido(request, id):
    api_url = BASE_URL + 'recorrido/recorrido/' + str(id) + '/'
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
            messages.success(request, 'Recorrido editado correctamente.')
            return redirect('recorridos')
        except requests.exceptions.RequestException as e:
            print(f'Error en la solicitud POST: {e}')
            messages.error(request, 'Error en la edición del recorrido, por favor intente nuevamente.')
            return redirect('recorridos')
    else:
        response = requests.get(api_url)
        recorrido = response.json()
        form = RecorridoApiForm(recorrido)
    editar = True
    return render(request, 'ProyectoHistoryArApp/crear_recorrido.html', {'form': form, 'editar': editar})

@staff_member_required
def eliminar_recorrido(request, id):
    api_url = BASE_URL + 'recorrido/' + 'estado_recorrido/' + str(id) + '/'
    csrftoken = get_token(request)
    headers = {
            'X-CSRFToken': csrftoken,
        }
    try:
        response = requests.put(api_url, headers=headers)
        response.raise_for_status()
        messages.success(request, 'Recorrido eliminado correctamente.')
        return redirect('recorridos')
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud DELETE: {e}')
        messages.error(request, 'Error en la eliminación del recorrido, por favor intente nuevamente.')
        return redirect('recorridos')

@staff_member_required
def detalle_recorrido(request, id):
    recorrido = get_json('recorrido/recorrido/' + str(id) + '/')
    return render(request, 'ProyectoHistoryArApp/detalle_recorrido.html', {'recorrido': recorrido})

@staff_member_required
def crear_recorrido(request):
    api_url = BASE_URL + 'recorrido/recorrido/'
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
                'activo': True,
            }

            try:
                response = requests.post(api_url, data=data, headers=headers)
                response.raise_for_status()
                messages.success(request, 'Recorrido creado correctamente.')
                return redirect('recorridos')
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud POST: {e}')
                messages.error(request, 'Error en la creacion del recorrido, por favor intente nuevamente.')
                return redirect('crear_recorrido')
        else:
            print(form.errors)
            messages.error(request, 'Error en la creacion del recorrido, revise los campos ingresados en el formulario.')
            return redirect('crear_recorrido')
    else:
        form = RecorridoApiForm()

    return render(request, 'ProyectoHistoryArApp/crear_recorrido.html', {'form': form})

#Puntos de Interes
@staff_member_required
def puntos_interes(request):
    #Puntos de Interes
    puntos_interes = get_json('puntoInteres/')

    page = request.GET.get('page', 1)
    buscar = request.GET.get('buscar')       
    paginator = Paginator(puntos_interes, 5)
    puntos_interes = paginator.get_page(page)
    if buscar is not None and buscar.strip():
        resultados = [punto for punto in puntos_interes if buscar.lower() in punto['nombre'].lower()]
        paginator = Paginator(resultados, 5)
        puntos_interes = paginator.get_page(page)
        return render(request, 'ProyectoHistoryArApp/puntos_interes.html', {'puntos_interes': puntos_interes, 'paginator': paginator, 'resultados': resultados})
    
    puntos_interes = paginator.get_page(page)
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
                'activo': True,
            }
            
            files = {}

            if 'modelo' in request.FILES:
                modelo_file = request.FILES['modelo']
                files['modelo'] = (modelo_file.name, modelo_file.read())

            
            if 'imagen' in request.FILES:
                imagen_file = request.FILES['imagen']
                files['imagen'] = (imagen_file.name, imagen_file.read())

            try:
                response = requests.post(api_url, data=data, headers=headers, files=files)
                response.raise_for_status()
                messages.success(request, 'Punto de interés creado correctamente.')
                return redirect('puntos_interes')
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud POST: {e}')
                messages.error(request, 'Error en la creación del punto de interés, por favor intente nuevamente.')
                return redirect('crear_punto_interes')
        else:
            print(form.errors)
            messages.error(request, 'Error en la creación del punto de interés, revise los campos ingresados en el formulario.')
            return redirect('crear_punto_interes')
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
                messages.success(request, 'Punto de interés editado correctamente.')
                return redirect('puntos_interes')
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud PUT: {e}')
                messages.error(request, 'Error en la edición del punto de interés, por favor intente nuevamente.')
                return redirect('puntos_interes')
    else:
        response = requests.get(api_url)
        punto = response.json()
        form = PuntosInteresForm(punto)

    editar = True
    return render(request, 'ProyectoHistoryArApp/crear_punto_interes.html', {'form': form, 'editar': editar})


@staff_member_required
def eliminar_punto_interes(request, id):
    api_url = BASE_URL + 'puntoInteres/' + 'estado_puntoInteres/' + str(id) + '/'
    csrftoken = get_token(request)
    headers = {
            'X-CSRFToken': csrftoken,
        }
    try:
        response = requests.put(api_url, headers=headers)
        response.raise_for_status()
        messages.success(request, 'Punto de interés eliminado correctamente.')
        return redirect('puntos_interes')
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud DELETE: {e}')
        messages.error(request, 'Error en la eliminación del punto de interés, por favor intente nuevamente.')
        return redirect('puntos_interes')

@staff_member_required
def detalle_punto_interes(request, id):
    punto = get_json('puntoInteres/' + str(id) + '/')
    return render(request, 'ProyectoHistoryArApp/detalle_punto_interes.html', {'punto': punto})


#Calificaciones
@staff_member_required
def eliminar_comentario(request, id, id_recorrido):
    api_url = BASE_URL + 'calificacion/' +  str(id) + '/' 
    csrftoken = get_token(request)
    headers = {
            'X-CSRFToken': csrftoken,
        }
    try:
        response = requests.delete(api_url, headers=headers)
        response.raise_for_status()
        messages.success(request, 'Comentario eliminado correctamente.')
        return HttpResponseRedirect(reverse('recorrido_detalle', args=[id_recorrido]))
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud DELETE: {e}')
        messages.error(request, 'Error en la eliminación del comentario, por favor intente nuevamente.')
        return HttpResponseRedirect(reverse('recorrido_detalle', args=[id_recorrido]))

#Transacciones
@staff_member_required
def transacciones(request):
    #Transacciones
    api_url = BASE_URL + 'transaccion/'
    response = requests.get(api_url)
    transacciones = response.json()
    
    #Paginación
    page = request.GET.get('page', 1)
    buscar = request.GET.get('buscar')       
    paginator = Paginator(transacciones, 5)
    transacciones = paginator.get_page(page)
    #Nombre de usuario
    for transaccion in transacciones:
        #Usuarios
        api_url_user = BASE_URL + 'usuario/' + 'usuarios/' + str(transaccion['usuario']) + '/'
        response_user = requests.get(api_url_user)
        usuarios = response_user.json()
        if usuarios['id'] == transaccion['usuario']:
            transaccion['usuario'] = usuarios['nombre']
            transaccion['email'] = usuarios['email']
            
    #Filtros
    if buscar:
        transacciones = [transaccion for transaccion in transacciones if buscar.lower() in transaccion['usuario'].lower() or buscar.lower() in transaccion['email'].lower()]
        paginator = Paginator(transacciones, 5)
        transacciones = paginator.page(page)
        return render(request, 'ProyectoHistoryArApp/transacciones.html', {'transacciones': transacciones, 'paginator': paginator})

    return render(request, 'ProyectoHistoryArApp/transacciones.html', {'transacciones': transacciones, 'paginator': paginator})

def obtener_init_point(request):
    url = 'https://api.mercadopago.com/checkout/preferences'
    params = {'id': request.user.id}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.MERCADO_PAGO_ACCESS_TOKEN}'
    }

    data = {
        "items": [
            {
                "title": "Suscripcion HistoryAr",
                "description": "Suscripcion mensual HistoryAr",
                "quantity": 1,
                "currency_id": "USD",
                "unit_price": 10,
            }
        ],
        "notification_url": f"https://tesis-web.onrender.com/api/transaccion/?id={request.user.id}",
        "back_urls": {
            "success": "https://tesis-web.onrender.com/success",
            "pending": "https://tesis-web.onrender.com/pending",
            "failure": "https://tesis-web.onrender.com/failure"
        },
        "auto_return": "approved",
    }
    response = requests.post(url, headers=headers, json=data, params=params)
    if response.status_code == 201:
        init_point = response.json().get('init_point')
        return init_point
    else:
        error_message = f'Error al obtener el init_point: {response.text}'
        return None, error_message

def verificar_firma(data, signature):
    # Generar la firma local utilizando la clave secreta de Mercado Pago
    secret = settings.MERCADO_PAGO_WEBHOOK_SECRET
    local_signature = hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()
    
    # Comparar la firma local con la firma recibida
    return hmac.compare_digest(local_signature, signature)

def success(request):
    return redirect('suscribirse')

def pending(request):
    return render(request, 'ProyectoHistoryArApp/pending.html')

def failure(request):
    return render(request, 'ProyectoHistoryArApp/failure.html')

def favoritos(request, id):
    id_usuario = request.user.id
    api_url = BASE_URL + 'usuario/' + 'usuario_favorito/' + str(id_usuario) + '/'
    response = requests.get(api_url)
    recorrido_original = response.json()['recorridoFavorito']
    if recorrido_original is not None and recorrido_original == id:
        data = {
            'recorridoFavorito': None,
        }
    else:
        data = {
            'recorridoFavorito': id,
        }

    csrftoken = get_token(request)
    
    headers = {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        }
    try:
        response = requests.put(api_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return redirect('recorrido')
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud PUT: {e}')
        return redirect('recorrido')

@login_required
def eliminar_favorito(request):
    id_usuario = request.user.id
    api_url = BASE_URL + 'usuario/' + 'usuario_favorito/' + str(id_usuario) + '/'

    data = {
        'recorridoFavorito': None,
    }

    csrftoken = get_token(request)
    
    headers = {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        }
    try:
        response = requests.put(api_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return redirect('perfil', id=id_usuario)
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud PUT: {e}')
        return redirect('perfil', id=id_usuario)
    
@login_required
def perfil(request,id):
    #Usuario
    api_url = BASE_URL + 'usuario/' + 'usuarios/' + str(id) + '/'
    response = requests.get(api_url)
    usuario = response.json()
    
    #Recorrido
    api_recorrido = BASE_URL + 'recorrido/'
    response_recorrido = requests.get(api_recorrido)
    recorridos = response_recorrido.json()


    ultimo_recorrido = ''
    recorrido = ''
            
    for recorrido in recorridos:
        if 'recorridoFavorito' in usuario and usuario['recorridoFavorito'] == recorrido['id'] and usuario['recorridoFavorito'] is not None:
            recorrido = recorrido
        if 'ultimosRecorridos' in usuario and usuario['ultimosRecorridos'] is not None:
            usuario['ultimosRecorridos'] = recorrido['nombre']

    if request.method == 'POST':
        api_url = BASE_URL + 'usuario/' + 'editar_usuario_nombre/' + str(request.user.id) + '/'
        csrftoken = get_token(request)
        headers = {
            'X-CSRFToken': csrftoken,
        }
        form = UsuarioPerfilForm(request.POST)
        if form.is_valid():
            data = {
                'nombre': form.cleaned_data['nombre'],
            }
            try:
                response = requests.put(api_url, data=data, headers=headers)
                response.raise_for_status()
                
                return render(request, 'ProyectoHistoryArApp/perfil.html', {'usuario': usuario, 'form': form, 'ultimo_recorrido': ultimo_recorrido, 'recorrido': recorrido})
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud PUT: {e}')
    else:
        form = UsuarioPerfilForm(usuario)
    return render(request, 'ProyectoHistoryArApp/perfil.html', {'usuario': usuario, 'form': form , 'recorrido': recorrido})

@login_required
def editar_imagen_perfil(request):
    api_url = BASE_URL + 'usuario/' + 'editar_imagen_usuario/' + str(request.user.id) + '/'
    csrftoken = get_token(request)
    headers = {
        'X-CSRFToken': csrftoken,
    }

    files = {}

    if request.method == 'POST':
        form = ImagenPerfilForm(request.POST, request.FILES)
        if form.is_valid():
            
            if 'imagen_update' in request.FILES:
                imagen_file = request.FILES['imagen_update']
                files['imagen_update'] = (imagen_file.name, imagen_file.read())

            try:
                response = requests.put(api_url, files=files, headers=headers)
                response.raise_for_status()
                return redirect('perfil', id=request.user.id)
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud PUT: {e}')
        else:
            print(form.errors)

    return redirect('perfil', id=request.user.id)

def contacto_email(request):
  if request.method == "POST":
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')

    template = render_to_string('ProyectoHistoryArApp/contacto_email.html', {
        'name': name,
        'email': email,
        'message': message
    })
    email = EmailMessage(
        subject,
        template,
        settings.EMAIL_HOST_USER,
        ['nicolaslabasse4@gmail.com']
    )

    email.fail_silently = False
    email.send()
    return redirect('gracias')

def gracias(request):
    return render(request, 'ProyectoHistoryArApp/gracias.html')


def get_json(endpoint):
    try:
        api_url = BASE_URL + endpoint
        response = requests.get(api_url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud GET: {e}')
        return None


