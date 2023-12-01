function actualizarEstadoFormulario(agotado) {
    var campos = [
        'input[name="nombreElemento"]',
        'input[name="disponibles"]',
        'input[name="valorUnidadElemento"]',
        'input[name="observacionesPrestamo"]',
        'input[type="file"]',
        'button[type="submit"]',
    ];

    campos.forEach(function (selector) {
        $(selector).prop('disabled', agotado);
        $(selector).css('background-color', agotado ? '#e0e0e0' : '');
    });
}

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

                    // Actualizar el campo de disponibles y el estado del formulario
                    if (response.esPrestado || response.Stock <= 0) {
                        actualizarEstadoFormulario(true); // Deshabilitar campos
                        $('input[name="disponibles"]').val(''); // Limpiar campo de disponibles
                    } else {
                        actualizarEstadoFormulario(false); // Habilitar campos
                        $('input[name="disponibles"]').val(response.Stock); // Mostrar stock disponible
                    }
                },
                error: function (xhr, status, error) {
                    console.error("Error: ", error);
                    // Limpiar los campos y deshabilitar si hay un error
                    $('input[name="nombreElemento"]').val('');
                    $('input[name="valorUnidadElemento"]').val('');
                    $('input[name="disponibles"]').val('');
                    actualizarEstadoFormulario(true);
                }
            });
        } else {
            // Limpiar y habilitar los campos si el serial está vacío
            $('input[name="nombreElemento"]').val('');
            $('input[name="valorUnidadElemento"]').val('');
            $('input[name="disponibles"]').val('');
            actualizarEstadoFormulario(false);
        }
    });
});

