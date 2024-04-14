document.addEventListener('DOMContentLoaded', function () {
    const registroForm = document.getElementById('registroForm');
    registroForm.addEventListener('submit', function (event) {
        event.preventDefault();
        if (validarFormulario()) {
            registroForm.submit();
            alert('Registro Exitoso');
        } else {
            console.log("Validación fallida.");
        }
    });
});

function validarFormulario() {
    const nombre = document.getElementById('nombre').value.trim();
    if (nombre === '') {
        alert('Por favor, ingrese su nombre.');
        return false;
    }

    const apellido = document.getElementById('apellido').value.trim();
    if (apellido === '') {
        alert('Por favor, ingrese su apellido.');
        return false;
    }

    const email = document.getElementById('email').value.trim();
    if (!isValidEmail(email)) {
        alert('Por favor, ingrese un correo electrónico válido.');
        return false;
    }

    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    if (password !== confirmPassword) {
        alert('Las contraseñas no coinciden.');
        return false;
    }
    if (!isValidPassword(password)) {
        alert('La contraseña debe tener al menos un número y una letra mayúscula, y tener entre 6 y 18 caracteres.');
        return false;
    }
    return true;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPassword(password) {
    const passwordRegex = /^(?=.*[0-9])(?=.*[A-Z])[a-zA-Z0-9]{6,18}$/;
    return passwordRegex.test(password);
}
