document.addEventListener("DOMContentLoaded", () => {

    const radioDenunciado = document.getElementById("tipo_denunciado");
    const radioSospechoso = document.getElementById("tipo_sospechoso");

    const divDenunciado = document.getElementById("denunciado");
    const divSospechosos = document.getElementById("sospechosos");

    const btnAgregar = document.getElementById("btnAgregar");
    // ✔ Mostrar/ocultar según el tipo seleccionado
    function actualizarVista() {
        if (radioDenunciado.checked) {
            divDenunciado.style.display = "block";
            divSospechosos.style.display = "none";
        } else if (radioSospechoso.checked) {
            divDenunciado.style.display = "none";
            divSospechosos.style.display = "block";
        }
    }

    radioDenunciado.addEventListener("change", actualizarVista);
    radioSospechoso.addEventListener("change", actualizarVista);

    // Iniciar ocultando ambos hasta que el usuario seleccione
    divDenunciado.style.display = "none";
    divSospechosos.style.display = "none";

    // ✔ Función para validar si los campos de un bloque están llenos
    function bloqueLleno(bloque) {
        const nombre = bloque.querySelector(".nombre").value.trim();
        const descripcion = bloque.querySelector(".descripcion").value.trim();

        return nombre !== "" && descripcion !== "";
    }

    // ✔ Agregar sospechoso dinámicamente
    btnAgregar.addEventListener("click", () => {

        const bloques = document.querySelectorAll(".sospechoso-item");
        const ultimoBloque = bloques[bloques.length - 1];

        // Verificar si el último bloque está lleno
        if (!bloqueLleno(ultimoBloque)) {
            alert("Debes completar los datos del sospechoso antes de agregar otro.");
            return;
        }

        // Crear nuevo bloque
        const nuevoBloque = document.createElement("div");
        nuevoBloque.classList.add("row", "two-cols", "sospechoso-item");

        nuevoBloque.innerHTML = `
            <div class="field">
                <label>Nombre</label>
                <input class="input nombre" name="nombre_sospechoso" type="text" required>
            </div>
            <div class="field">
                <label>Descripción</label>
                <textarea class="input descripcion" name="descripcion_sospechoso" required></textarea>
            </div>
        `;

        divSospechosos.appendChild(nuevoBloque);
        
    });
    actualizarVista();

});
