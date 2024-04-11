document.addEventListener('DOMContentLoaded', function () {
    var registroForm = document.getElementById('editarCuentaForm');
    registroForm.addEventListener('submit', function (event) {
        event.preventDefault();
        if (alMenosUnCampoValido()) {
            alert('Formulario enviado correctamente');
            registroForm.submit(); // Envía el formulario si al menos un campo es válido
        } else {
            alert('Por favor, complete al menos un campo correctamente.');
        }
    });
});

function alMenosUnCampoValido() {
    var usuario = document.getElementById('usuario').value.trim();
    if (usuario !== '') {
        return true;
    }

    var email = document.getElementById('email').value.trim();
    if (isValidEmail(email)) {
        return true;
    }

    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;
    if ((password !== '' && confirmPassword !== '') && (password === confirmPassword) && isValidPassword(password)) {
        return true;
    } else {
        alert('Las contraseñas no coinciden.');
        return false;
    }

    return false;
}

function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPassword(password) {
    var passwordRegex = /^(?=.*[0-9])(?=.*[A-Z])[a-zA-Z0-9]{6,18}$/;
    return passwordRegex.test(password);
}
