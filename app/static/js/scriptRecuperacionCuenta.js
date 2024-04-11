$(document).ready(function(){
    // Manejo del envío del formulario
    $("#passwordRecoveryForm").submit(function(event){
      // Prevenir el envío del formulario
      event.preventDefault();
      
      // Obtener el correo electrónico ingresado por el usuario
      var email = $("#email").val();
      
      // Aquí puedes agregar lógica adicional, como enviar una solicitud al servidor para generar una nueva contraseña
      
      // Por ahora, simplemente mostramos un mensaje de éxito
      alert("Se ha enviado un correo electrónico para restablecer tu contraseña a: " + email);
    });
  });
  