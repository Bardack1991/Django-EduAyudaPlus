from django.shortcuts import render

def editarCuenta(request):
    return render(request, 'app/editarcuenta.html')

def registro(request):
    return render(request, 'app/formularioRegistro.html')

def inicio(request):
    return render(request, 'app/inicio.html')

def inicioSesion(request):
    return render(request, 'app/iniciosesion.html')

def menuUsuario(request):
    return render(request, 'app/menuUsuario.html')

def recuperarCuenta(request):
    return render(request, 'app/recuperacionCuenta.html')