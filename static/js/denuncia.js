// Función para buscar persona por DNI y mostrar resultados
async function buscarPersonaPorDNI(dni) {
    try {
        console.log("Buscando persona con DNI:", dni); // 🔹 prueba en consola

        const response = await fetch(`/persona_dni/${dni}/json`);
        const result = await response.json();

        console.log("Resultado completo del API:", result); // 🔹 muestra todo

        if (result.status === 1 && result.data) {
            const persona = result.data;

            console.log("Persona encontrada:", persona);

            // Asignar todos los campos, incluso si son null o undefined
            const campos = ["nombres","ape_paterno","ape_materno","fecha_nacimiento","telefono","direccion"];
            campos.forEach(id => {
                const input = document.getElementById(id);
                if (input) input.value = persona[id] ?? "";
            });

            alert(`Persona encontrada: ${persona.nombres} ${persona.ape_paterno}\nTel: ${persona.telefono ?? "N/A"}\nDir: ${persona.direccion ?? "N/A"}`);

        } else {
            console.warn("Persona no encontrada");
            alert(result.message ?? "Persona no encontrada");

            // Limpiar formulario
            ["nombres","ape_paterno","ape_materno","fecha_nacimiento","telefono","direccion"].forEach(id => {
                const input = document.getElementById(id);
                if (input) input.value = "";
            });
        }

    } catch (error) {
        console.error("Error al buscar persona:", error);
        alert("Ocurrió un error al buscar la persona. Revisar consola para más detalles.");
    }
}

// Esperar a que el DOM cargue para agregar eventos
document.addEventListener("DOMContentLoaded", () => {
    const dniInput = document.getElementById("dni");

    if (!dniInput) {
        console.error("No se encontró el input con id 'dni'");
        return;
    }

    dniInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault(); // evita que el formulario se envíe
            const dni = dniInput.value.trim();
            if (dni) {
                buscarPersonaPorDNI(dni);
            } else {
                console.warn("El campo DNI está vacío");
                alert("Ingrese un DNI para buscar");
            }
        }
    });
});
