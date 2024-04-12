from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def editarCuenta(request):
    return render(request, 'app/editarcuenta.html')

def registro(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        password = request.POST['password']
        confirmar_password = request.POST['confirmPassword']

        if password != confirmar_password:
            return render(request, 'app/formularioRegistro.html', {'error': 'Las contraseñas no coinciden'})

        user = User.objects.create_user(username=email, email=email, password=password, first_name=nombre, last_name=apellido)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        return redirect('inicio')  
    else:
        return render(request, 'app/formularioRegistro.html')

def inicio(request):
    return render(request, 'app/inicio.html')

def inicioSesion(request):
    return render(request, 'app/iniciosesion.html')

def menuUsuario(request):
    return render(request, 'app/menuUsuario.html')

def recuperarCuenta(request):
    return render(request, 'app/recuperacionCuenta.html')