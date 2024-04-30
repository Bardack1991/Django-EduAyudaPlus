# Django-EduAyudaPlus
Proyecto migrado desde html, css y javascript a Django
    -Este proyecto utiliza las API de OPENAI Y GOOGLE CLOUD SERVICES (Bucket) para su funcionamiento.

# Preparar archivo .env

ubicar el archivo .env en la raiz del proyecto, este debe incluir las siguientes variables.

    OPENAI_API_KEY="TU LLAVE DE OPEN AI"
    GOOGLE_APPLICATION_CREDENTIALS="RUTA A TU ARCHIVO JSON CON LAS CREDENCIALES DE GOOGLE"

# Crear tablas db

Correr el siguente comando, para crear las tablas necesarias para el funcionamiento de la app.

    python manage.py migrate

# Poblar tablas

Usar el siguiente SQL para insertar informacion a las tablas

    INSERT INTO APP_SERVICIO
    (ID, NOMBRE_SERVICIO, DESCRIPCION, PRECIO)
    VALUES(1, 'Texto a voz', 'Texto a voz
    ', 1000);
    INSERT INTO APP_SERVICIO
    (ID, NOMBRE_SERVICIO, DESCRIPCION, PRECIO)
    VALUES(2, 'Voz a texto', 'Voz a texto', 1000);

# Ejecutar el proyecto

    python manage.py runserver

