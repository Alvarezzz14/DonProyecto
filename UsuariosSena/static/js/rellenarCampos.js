$(document).ready(function () {
    // Cuando se cambia el número de serial
    $(document).ready(function () {
        $('input[name="serialSenaElemento"]').on('input', function () {
            var serialNumber = $(this).val();
            if (serialNumber) {
                $.ajax({
                    url: '/get-element-name-by-serial',
                    type: 'GET',
                    data: { 'serialNumber': serialNumber },
                    success: function (response) {
                        // Actualizar los campos
                        $('input[name="nombreElemento"]').val(response.elementName);
                        $('input[name="valorUnidadElemento"]').val(response.valorUnidad);
                        $('input[name="disponibles"]').val(response.Stock);
                    },
                    error: function (xhr, status, error) {
                        console.error("Error: ", error);
                        // Limpiar los campos si hay un error
                        $('input[name="nombreElemento"]').val('');
                        $('input[name="valorUnidadElemento"]').val('');
                        $('input[name="disponibles"]').val('');
                    }
                });
            } else {
                // Limpiar los campos si el número de serie está vacío
                $('input[name="nombreElemento"]').val('');
                $('input[name="valorUnidadElemento"]').val('');
                $('input[name="disponibles"]').val('');
            }
        });
    });
});

//AVISO CANCELAR
function confirmCancel() {
    Swal.fire({
        title: '¿Estás seguro de que quieres cancelar?',
        text: "Esta acción no se puede deshacer.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cancelar',
        cancelButtonText: 'No, volver'
    }).then((result) => {
        if (result.isConfirmed) {
            document.querySelector('.form').reset();
        }
    });
}