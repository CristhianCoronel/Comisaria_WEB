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
