// registrar_denuncia.js

// ======= BUSCAR PERSONA POR DNI =======
async function buscarPersonaPorDNI(dni) {
    try {
        const response = await fetch(`/persona_dni/${dni}/json`);
        const result = await response.json();

        if (result.status === 1 && result.data) {
            const persona = result.data;
            const campos = ["nombres","ape_paterno","ape_materno","fecha_nacimiento","telefono","direccion"];
            campos.forEach(id => {
                const input = document.getElementById(id);
                if (input) input.value = persona[id] ?? "";
            });
            alert(`Persona encontrada: ${persona.nombres} ${persona.ape_paterno}`);
        } else {
            alert(result.message ?? "Persona no encontrada");
            ["nombres","ape_paterno","ape_materno","fecha_nacimiento","telefono","direccion"].forEach(id => {
                const input = document.getElementById(id);
                if (input) input.value = "";
            });
        }
    } catch (error) {
        console.error("Error al buscar persona:", error);
        alert("Error al buscar persona. Revisar consola.");
    }
}

// ======= AGREGAR EVIDENCIA A LA TABLA =======
function agregarEvidencia() {
    const tipo = document.getElementById('tipo_evidencia').value;
    const archivo = document.getElementById('archivo_evidencia').files[0];
    const descripcion = document.getElementById('descripcion_evidencia').value;

    if (!tipo || !archivo) {
        alert('Seleccione tipo y archivo de evidencia');
        return;
    }

    const tbody = document.getElementById('evidencias-table-body');
    const row = document.createElement('tr');

    // Guardamos archivo en un input hidden temporalmente
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.files = [archivo];
    fileInput.name = 'evidencia_archivo[]';
    fileInput.style.display = 'none';

    row.innerHTML = `
        <td><input type="hidden" name="evidencia_tipo[]" value="${tipo}">${tipo}</td>
        <td>${archivo.name}</td>
        <td><input type="hidden" name="evidencia_descripcion[]" value="${descripcion}">${descripcion}</td>
        <td><button type="button" class="btn btn-danger">Eliminar</button></td>
    `;
    row.appendChild(fileInput);
    tbody.appendChild(row);

    // Botón eliminar
    row.querySelector('button').addEventListener('click', () => row.remove());

    // Limpiar campos
    document.getElementById('tipo_evidencia').value = '';
    document.getElementById('archivo_evidencia').value = '';
    document.getElementById('descripcion_evidencia').value = '';
}

// ======= ENVIAR FORMULARIO =======
async function enviarFormulario() {
    const form = document.querySelector('form');
    const formData = new FormData();

    // Campos denunciante
    ["dni","nombres","ape_paterno","ape_materno","fecha_nacimiento","telefono","direccion"].forEach(id => {
        const input = document.getElementById(id);
        if (input) formData.append(id, input.value);
    });

    // Campos denuncia
    formData.append('fecha_incidente', form.querySelector('input[name="fecha_incidente"]').value);
    formData.append('hora_incidente', form.querySelector('input[name="hora_incidente"]').value);
    formData.append('direccion_incidente', form.querySelector('input[placeholder*="frente al banco"]').value);
    formData.append('tipo_denuncia', form.querySelector('select[name="tipo_denuncia"]').value);
    formData.append('descripcion', form.querySelector('input[name="descripcion"]').value);

    // Evidencias
    const tbody = document.getElementById('evidencias-table-body');
    tbody.querySelectorAll('tr').forEach(row => {
        const tipo = row.querySelector('input[name="evidencia_tipo[]"]').value;
        const desc = row.querySelector('input[name="evidencia_descripcion[]"]').value;
        const fileInput = row.querySelector('input[type="file"]');
        if (fileInput && fileInput.files[0]) {
            formData.append('evidencia_tipo[]', tipo);
            formData.append('evidencia_descripcion[]', desc);
            formData.append('evidencia_archivo[]', fileInput.files[0]);
        }
    });

    try {
        const response = await fetch('/registrar_denuncia', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.status === 1) {
            alert('Denuncia registrada correctamente');
            window.location.reload();
        } else {
            alert(result.message ?? 'Error al registrar denuncia');
        }
    } catch (error) {
        console.error('Error al enviar formulario:', error);
        alert('Error al enviar formulario. Revisar consola.');
    }
}

// ======= EVENT LISTENERS =======
document.addEventListener('DOMContentLoaded', () => {
    const dniInput = document.getElementById("dni");
    if (dniInput) {
        dniInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                const dni = dniInput.value.trim();
                if (dni) buscarPersonaPorDNI(dni);
                else alert("Ingrese un DNI para buscar");
            }
        });
    }

    const agregarBtn = document.getElementById('agregar-evidencia-btn');
    if (agregarBtn) agregarBtn.addEventListener('click', agregarEvidencia);

    const registrarBtn = document.querySelector('button[type="button"]:first-of-type');
    if (registrarBtn) registrarBtn.addEventListener('click', enviarFormulario);
});
