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
document.getElementById('agregar-evidencia-btn').addEventListener('click', () => {
    const tipo = document.getElementById('tipo_evidencia').value;
    const archivo = document.getElementById('archivo_evidencia').files[0];
    const descripcion = document.getElementById('descripcion_evidencia').value;

    if (!tipo || !archivo) {
        alert('Seleccione tipo y archivo de evidencia');
        return;
    }

    const tbody = document.getElementById('evidencias-table-body');
    const row = document.createElement('tr');

    row.innerHTML = `
        <td>${tipo}</td>
        <td>${archivo.name}</td>
        <td>${descripcion}</td>
        <td><button type="button" class="btn btn-danger" onclick="this.closest('tr').remove()">Eliminar</button></td>
    `;
    tbody.appendChild(row);

    // Limpiar campos
    document.getElementById('tipo_evidencia').value = '';
    document.getElementById('archivo_evidencia').value = '';
    document.getElementById('descripcion_evidencia').value = '';
});


let currentStep = 1;
const totalSteps = 3;

function showStep(step) {
    for (let i = 1; i <= totalSteps; i++) {
        document.getElementById(`step-${i}`).style.display = (i === step) ? 'block' : 'none';
    }
    currentStep = step;
}

function nextStep() {
    if (currentStep < totalSteps) showStep(currentStep + 1);
}

function prevStep() {
    if (currentStep > 1) showStep(currentStep - 1);
}

// Ejemplo: Autocompletar nombre según DNI
document.getElementById('dni').addEventListener('keyup', function(e) {
    if (e.key === "Enter") {
        const dni = e.target.value;
        // Aquí se llamaría a tu API/función para traer datos
        // Ejemplo ficticio:
        document.getElementById('nombres').value = "Juan Pérez López"; 
    }
});

// Aquí puedes agregar la lógica para cargar el paso 2 según el tipo de denuncia
document.getElementById('tipo_denuncia')?.addEventListener('change', function() {
    const tipo = this.value;
    const contenedor = document.getElementById('datos-tipo-denuncia');
    if(tipo === "1") { // Hurto
        fetch('/templates/denuncia_hurto.html')
            .then(resp => resp.text())
            .then(html => contenedor.innerHTML = html);
    } else {
        contenedor.innerHTML = ""; // Otros tipos
    }
});
