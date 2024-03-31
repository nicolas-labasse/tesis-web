import requests


"""BASE_URL = 'https://tesis-web.onrender.com/api/'"""
BASE_URL = 'http://192.168.1.2:8081/api/'


def custom_context(request):
    try:
        user_email = request.user.email

        api_url = BASE_URL + 'usuario/' + 'usuarios/'
        response = requests.get(api_url)
        usuarios = response.json()

        imagen_usuario = ''

        for usuario in usuarios:
            if usuario.get('email') == user_email:
                imagen_usuario = usuario.get('imagen')
                break

        return {'imagen_usuario': imagen_usuario}
    except Exception as e:
        print(f"Error en custom_context: {e}")
        return {'imagen_usuario': ''}
    

def custom_nombre_usuario(request):
    try:
        user_email = request.user.email

        api_url = BASE_URL + 'usuario/' + 'usuarios/'
        response = requests.get(api_url)
        usuarios = response.json()

        nombre_usuario = ''

        for usuario in usuarios:
            if usuario.get('email') == user_email:
                nombre_usuario = usuario.get('nombre')
                break

        return {'nombre_usuario': nombre_usuario}
    except Exception as e:
        print(f"Error en custom_nombre_usuario: {e}")
        return {'nombre_usuario': ''}