import os
import shutil 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ArchivosUsuario, HistorialServicios, Servicio
from django.http import HttpResponse
from openai import OpenAI
from pathlib import Path
from google.cloud import storage
from dotenv import load_dotenv
import tempfile

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

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
            url_archivo='',
            nombre_archivo=nombre_archivo,
            tipo_servicio=servicio,
            id_usuario=request.user,
            fecha_subida=timezone.now()
        )
        
        HistorialServicios.objects.create(
            fecha_servicio=timezone.now(),
            servicio=servicio,
            id_usuario=request.user,
            archivo_usuario=archivo_usuario
        )

        supported_formats = ['mp3', 'txt']
        file_extension = archivo.name.split('.')[-1]

        if file_extension not in supported_formats:
            messages.error(request, "Formato de archivo no soportado.")
            return redirect('carga-archivo')

        if servicio_id == '1':  #Voz a texto
            with tempfile.NamedTemporaryFile(delete=False, suffix='.' + archivo.name.split('.')[-1]) as tmp:
                for chunk in archivo.chunks():
                    tmp.write(chunk)
                tmp_path = Path(tmp.name)

            client = OpenAI()
            try:
                with open(tmp_path, 'rb') as audio_file:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                text_content = transcription.text

                text_file_path = Path('media') / f'{nombre_archivo}.txt'
                with open(text_file_path, 'w') as text_file:
                    text_file.write(text_content)
                
                bucket_name = 'eduayuda_bucket'
                public_url = upload_to_gcs(bucket_name, str(text_file_path), f'{nombre_archivo}.txt')
                if public_url:
                    make_blob_public(bucket_name, f'{nombre_archivo}.txt')
                    archivo_usuario.url_archivo = public_url
                    archivo_usuario.save()

            finally:
                if tmp_path.exists():
                    tmp_path.unlink()
                if text_file_path.exists():
                    text_file_path.unlink()

        if servicio_id == '2': #Texto a voz
            file_content = archivo.read().decode('utf-8')
            client = OpenAI()
            response = client.audio.speech.create(
              model="tts-1",
              voice="alloy",
              input=file_content
            )
            
            media_path = Path('media')
            media_path.mkdir(parents=True, exist_ok=True)

            speech_file_path = media_path / f'{nombre_archivo}.mp3'
            response.stream_to_file(str(speech_file_path))

            bucket_name = 'eduayuda_bucket'
            file_name = f'{nombre_archivo}.mp3'
            public_url = upload_to_gcs(bucket_name, str(speech_file_path), f'{nombre_archivo}.mp3')
            if public_url:
                print(f"URL obtenida de GCS: {public_url}")
                make_blob_public(bucket_name, file_name)
                archivo_usuario.url_archivo = public_url
                archivo_usuario.save()
                print(f"URL almacenada en la base de datos: {archivo_usuario.url_archivo}")
                try:
                    os.remove(str(speech_file_path))
                except OSError as e:
                    print(f"Error al eliminar el archivo {speech_file_path}: {e}")
            else:
                print("No se pudo obtener la URL de GCS.")
            archivo_usuario.url_archivo = public_url
            archivo_usuario.save()

        return redirect('menu-usuario')
    else:
        return render(request, 'app/inicio.html')

    
@login_required
def eliminar_archivo(request, archivo_id):
    if request.method == 'POST':
        archivo = get_object_or_404(ArchivosUsuario, id=archivo_id, id_usuario=request.user)
        archivo.delete()
        return redirect('menu-usuario')
    else:
        return HttpResponse("Método no permitido", status=405)

""" Utils """

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        public_url = f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"
        print(f"Archivo subido exitosamente: {public_url}")
        return public_url
    except Exception as e:
        print(f"Error al subir archivo a Google Cloud Storage: {str(e)}")
        return None
    
def make_blob_public(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.make_public()

    print(f"Blob {blob_name} is now publicly accessible at {blob.public_url}")