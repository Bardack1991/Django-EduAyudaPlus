document.addEventListener('DOMContentLoaded', function () {
    var registroForm = document.getElementById('registroForm');
    registroForm.addEventListener('submit', function (event) {
        console.log(event.data);
        event.preventDefault();
        if (validarFormulario()) {
            alert('Formulario enviado correctamente');
        }
    });
});

function validarFormulario() {
    var nombre = document.getElementById('nombre').value.trim();
    if (nombre === '') {
        alert('Por favor, ingrese su nombre completo.');
        return false;
    }

    var usuario = document.getElementById('usuario').value.trim();
    if (usuario === '') {
        alert('Por favor, ingrese un nombre de usuario.');
        return false;
    }

    var email = document.getElementById('email').value.trim();
    if (!isValidEmail(email)) {
        alert('Por favor, ingrese un correo electrónico válido.');
        return false;
    }

    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;
    if (password === '' || confirmPassword === '') {
        alert('Por favor, complete ambos campos de contraseña.');
        return false;
    }
    if (password !== confirmPassword) {
        alert('Las contraseñas no coinciden.');
        return false;
    }
    if (!isValidPassword(password)) {
        alert('La contraseña debe tener al menos un número y una letra mayúscula, y tener entre 6 y 18 caracteres.');
        return false;
    }

    var fechaNacimiento = document.getElementById('fechaNacimiento').value;
    if (!fechaNacimiento) {
        alert('Debe ingresar su fecha de nacimiento.');
        return false;
    }
    var fechaNacimientoDate = new Date(fechaNacimiento);
    var hoy = new Date();
    var edad = hoy.getFullYear() - fechaNacimientoDate.getFullYear();
    var mes = hoy.getMonth() - fechaNacimientoDate.getMonth();
    if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNacimientoDate.getDate())) {
        edad--;
    }
    if (edad < 13) {
        alert('Debes tener al menos 13 años para registrarte.');
        return false;
    }
    return true;
}

function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPassword(password) {
    var passwordRegex = /^(?=.*[0-9])(?=.*[A-Z])[a-zA-Z0-9]{6,18}$/;
    return passwordRegex.test(password);
}
