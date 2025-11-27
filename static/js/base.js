const menuToggle = document.getElementById("menu-toggle");
const dropdown = document.getElementById("dropdown-menu");

menuToggle.addEventListener("click", (e) => {
  e.stopPropagation(); 
  dropdown.classList.toggle("hidden");
});

document.addEventListener("click", () => {
  dropdown.classList.add("hidden");
});

dropdown.addEventListener("click", (e) => e.stopPropagation());

document.addEventListener("DOMContentLoaded", () => {
    const messages = document.querySelectorAll(".notification");

    if (messages.length > 0) {
        let container = document.querySelector(".toast-container");
        if (!container) {
            container = document.createElement("div");
            container.classList.add("toast-container");
            document.body.appendChild(container);
        }

        messages.forEach(msg => {
            const toast = document.createElement("div");
            toast.className = "toast " + msg.className.replace("notification", "").trim();
            toast.textContent = msg.textContent.trim();

            container.appendChild(toast);

            setTimeout(() => {
                toast.classList.add("hide");
                setTimeout(() => toast.remove(), 400);
            }, 4000);
        });
    }
});
