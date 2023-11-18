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