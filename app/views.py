from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ArchivosUsuario, HistorialServicios, Servicio
from django.http import HttpResponse

@login_required(login_url='inicio-sesion')
def editarCuenta(request):
    if request.method == 'POST':
        usuario = request.user
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar_password = request.POST.get('confirmPassword')

        if email and email != usuario.email:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está en uso')
                return render(request, 'app/editarcuenta.html')
            else:
                usuario.email = email

        if password and confirmar_password:
            if password != confirmar_password:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'app/editarcuenta.html')
            else:
                usuario.set_password(password)

        usuario.save()
        messages.success(request, 'Tu cuenta ha sido actualizada exitosamente')
        if password:
            login(request, usuario)
        return redirect('menu-usuario')
    else:
        return render(request, 'app/editarcuenta.html')

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar_password = request.POST.get('confirmPassword')

        if password != confirmar_password:
            return render(request, 'app/formularioRegistro.html', {'error': 'Las contraseñas no coinciden'})

        if User.objects.filter(email=email).exists():
            return render(request, 'app/formularioRegistro.html', {'error': 'Ya existe un usuario con ese correo electrónico'})

        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=nombre, last_name=apellido)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            return redirect('inicio')
        except IntegrityError:
            return render(request, 'app/formularioRegistro.html', {'error': 'Este nombre de usuario ya está en uso'})
    else:
        return render(request, 'app/formularioRegistro.html')

def inicio(request):
    return render(request, 'app/inicio.html')

def inicioSesion(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu-usuario')
        else:
            print("Fallo de autenticación")
            return render(request, 'app/iniciosesion.html', {'error': 'Correo electrónico o contraseña inválido'})
    return render(request, 'app/iniciosesion.html')

@login_required(login_url='inicio-sesion')
def menuUsuario(request):
    user = request.user
    archivos = ArchivosUsuario.objects.filter(id_usuario=request.user).select_related('tipo_servicio')
    if not user.is_authenticated:
        return redirect('inicio-sesion')
    return render(request, 'app/menuUsuario.html', {'user': request.user, 'archivos': archivos})

def recuperarCuenta(request):
    return render(request, 'app/recuperacionCuenta.html')

def logout_view(request):
    logout(request)
    return redirect('inicio')

@login_required
def carga_archivo(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        nombre_archivo = request.POST.get('nombreArchivo')
        servicio_id = request.POST.get('servicio')
        servicio = get_object_or_404(Servicio, pk=servicio_id)
        
        archivo_usuario = ArchivosUsuario.objects.create(
            url_archivo='prueba',
            nombre_archivo=nombre_archivo,
            tipo_servicio=servicio,
            id_usuario=request.user,
            fecha_subida=timezone.now()
        )
        
        # Registrar el servicio en el historial
        HistorialServicios.objects.create(
            fecha_servicio=timezone.now(),
            servicio=servicio,
            id_usuario=request.user,
            archivo_usuario=archivo_usuario
        )
        
        return redirect('menu-usuario')
    else:
        return render(request, 'app/inicio.html')

    
@login_required
def eliminar_archivo(request, archivo_id):
    if request.method == 'POST':
        archivo = get_object_or_404(ArchivosUsuario, id=archivo_id, id_usuario=request.user)
        archivo.delete()
        return redirect('menu-usuario')  # Redirige a la vista que muestra los archivos
    else:
        return HttpResponse("Método no permitido", status=405)