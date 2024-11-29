


 document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('');
    
    form.addEventListener('submit', function (event) {
        event.preventDefault();  // Evita el envío del formulario

        Swal.fire({
            title: "¿Quieres guardar los cambios?",
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: "Guardar",
            denyButtonText: "No guardar"
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire("¡Guardado!", "", "success");
            } else if (result.isDenied) {
                Swal.fire("Los cambios no se guardaron", "", "info");
            }
        });
    });
 });