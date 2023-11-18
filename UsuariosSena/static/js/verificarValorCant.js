$(document).ready(function () {
    // Verificar si el valor es un número entero positivo
    $('#cantidadElemento').on('input', function () {
        var value = $(this).val();
        if (!/^\d+$/.test(value)) { //Verifica si el valor es un número entero positivo
            $(this).val(''); // Restablecer al valor predeterminado si no es un entero positivo
        } else {
            var intValue = parseInt(value);
            if (intValue <= 0) {
                $(this).val('1'); // Restablecer al valor predeterminado si es cero o negativo
            }
        }
    });
});