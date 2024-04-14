$(document).ready(function(){
    $("#passwordRecoveryForm").submit(function(event){
      event.preventDefault();
      var email = $("#email").val();
      alert("Se ha enviado un correo electrónico para restablecer tu contraseña a: " + email);
    });
  });
  