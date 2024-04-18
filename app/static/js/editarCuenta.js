document.addEventListener('DOMContentLoaded', function () {
    var registroForm = document.getElementById('editarCuentaForm');
    registroForm.addEventListener('submit', function (event) {
        event.preventDefault();
        if (alMenosUnCampoValido()) {
            alert('Formulario enviado correctamente');
            registroForm.submit();
        } else {
            alert('Por favor, complete al menos un campo correctamente.');
        }
    });
});

function alMenosUnCampoValido() {
    var email = document.getElementById('email').value.trim();
    if (isValidEmail(email)) {
        return true;
    }

    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;
    if (password !== '' && confirmPassword !== '' && password === confirmPassword) {
        if (isValidPassword(password)) {
            return true;
        } else {
            alert('La contraseña debe tener al menos un número y una letra mayúscula, y tener entre 6 y 18 caracteres.');
            return false;
        }
    } else {
        if (password !== confirmPassword) {
            alert('Las contraseñas no coinciden.');
        }
        return false;
    }
}

function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPassword(password) {
    var passwordRegex = /^(?=.*[0-9])(?=.*[A-Z])[a-zA-Z0-9]{6,18}$/;
    return passwordRegex.test(password);
}

function togglePasswordVisibility() {
    var passwordInput = document.getElementById('password');
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}
