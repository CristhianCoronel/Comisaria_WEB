// Función para buscar persona por DNI y mostrar resultados
async function buscarPersonaPorDNI(dni) {
    try {
        // Llamada a la API
        const response = await fetch(`/persona/${dni}/json`);

        // Verificamos si la respuesta HTTP fue OK
        if (!response.ok) {
            const errorData = await response.json();
            console.error("Error HTTP:", response.status, errorData.message);
            alert(errorData.message);
            return;
        }

        const result = await response.json();

        // Comprobamos el estado de la API
        if (result.status === 1 && result.data) {
            const persona = result.data;
            
            // Mostramos los datos en el formulario o consola
            console.log("Persona encontrada:", persona);
            document.getElementById("nombres").value = persona.nombres || "";
            document.getElementById("ape_paterno").value = persona.ape_paterno || "";
            document.getElementById("ape_materno").value = persona.ape_materno || "";
            document.getElementById("fecha_nacimiento").value = persona.fecha_nacimiento || "";
            document.getElementById("telefono").value = persona.telefono || "";
            document.getElementById("direccion").value = persona.direccion || "";

        } else if (result.status === 0) {
            console.warn("Persona no encontrada");
            alert(result.message);
            // Limpiar formulario si no se encuentra
            document.getElementById("nombres").value = "";
            document.getElementById("ape_paterno").value = "";
            document.getElementById("ape_materno").value = "";
            document.getElementById("fecha_nacimiento").value = "";
            document.getElementById("telefono").value = "";
            document.getElementById("direccion").value = "";
        }

    } catch (error) {
        console.error("Error al buscar persona:", error);
        alert("Ocurrió un error al buscar la persona.");
    }
}

// Ejemplo de uso, con botón o evento
document.getElementById("buscarDNI").addEventListener("click", () => {
    const dni = document.getElementById("dniInput").value.trim();
    if (dni) buscarPersonaPorDNI(dni);
});
