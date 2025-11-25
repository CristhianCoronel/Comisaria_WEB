const menuToggle = document.getElementById("menu-toggle");
const dropdown = document.getElementById("dropdown-menu");

menuToggle.addEventListener("click", (e) => {
  e.stopPropagation(); // evita que el clic cierre inmediatamente
  dropdown.classList.toggle("hidden");
});

// Cerrar al clicar fuera
document.addEventListener("click", () => {
  dropdown.classList.add("hidden");
});

// Evita que clicar dentro del dropdown lo cierre
dropdown.addEventListener("click", (e) => e.stopPropagation());

document.addEventListener("DOMContentLoaded", () => {
    const messages = document.querySelectorAll(".notification");

    if (messages.length > 0) {
        // Crear contenedor flotante si no existe
        let container = document.querySelector(".toast-container");
        if (!container) {
            container = document.createElement("div");
            container.classList.add("toast-container");
            document.body.appendChild(container);
        }

        messages.forEach(msg => {
            // Convertir las notificaciones existentes en "toast"
            const toast = document.createElement("div");
            toast.className = "toast " + msg.className.replace("notification", "").trim();
            toast.textContent = msg.textContent.trim();

            container.appendChild(toast);

            // Tiempo de cierre automático (4 segundos)
            setTimeout(() => {
                toast.classList.add("hide");
                setTimeout(() => toast.remove(), 400);
            }, 4000);
        });
    }
});
