const togglePassword = () => {
    const passwordField = document.getElementById("psw");
    const passwordToggle = document.querySelector(".toggle-password");
    const passwordIcon = document.querySelector(".toggle-password i");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        passwordIcon.classList.remove("fa-eye");
        passwordIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        passwordIcon.classList.remove("fa-eye-slash");
        passwordIcon.classList.add("fa-eye");
    }
};

const togglePasswordBtn = document.querySelector(".toggle-password");
togglePasswordBtn.addEventListener("click", togglePassword);
/*CAMBIA DE COLOR EL ICONO DEL DROPDOWN LIST*/
const selectElement = document.getElementById("id-type");
const iconContainer = document.querySelector(".icon-container");

selectElement.addEventListener("change", function () {
    iconContainer.classList.add("selected"); // agregar la clase al icon-container
    setTimeout(function () {
        iconContainer.classList.remove("selected"); // restablecer el color del icono después de 1 segundo
    }, 1000);
});