document.addEventListener('DOMContentLoaded', function () {
    var loginForm = document.getElementById('formulario-login');
    loginForm.addEventListener('submit', function (event) {
        console.log(event.data);
        event.preventDefault();
        if (validarFormulario()) {
            alert('Formulario enviado correctamente');
        }
    });
});

function validarFormulario() {
    var email = document.getElementById('email').value.trim();
    if (!isValidEmail(email)) {
        alert('Por favor, ingrese un correo electrónico válido.');
        return false;
    }

    var password = document.getElementById('password').value;
    if (password === '' ) {
        alert('Por favor, complete el campo de contraseña.');
        return false;
    }
    if (!isValidPassword(password)) {
        alert('La contraseña debe tener al menos un número y una letra mayúscula, y tener entre 6 y 18 caracteres.');
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
