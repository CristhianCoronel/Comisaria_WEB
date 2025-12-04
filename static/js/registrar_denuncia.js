// ==============================
// Utilidades
// ==============================
function showAlert(msg) {
    alert(msg); // luego puedes cambiar por SweetAlert2 si quieres
}

// ==============================
// Control de pasos
// ==============================
let currentStep = 1;
const totalSteps = 3;

function updateStepIndicator(step) {
    document.querySelectorAll('.step-item').forEach(el => {
        const s = parseInt(el.dataset.step, 10);
        if (s === step) el.classList.add('active');
        else el.classList.remove('active');
    });
}

function showStep(step) {
    for (let i = 1; i <= totalSteps; i++) {
        const div = document.getElementById(`step-${i}`);
        if (!div) continue;
        div.style.display = (i === step) ? 'block' : 'none';
    }
    currentStep = step;
    updateStepIndicator(step);
}

// Validaciones mínimas por paso
function validateStep(step) {
    if (step === 1) {
        const dni = document.getElementById('dni').value.trim();
        const nombres = document.getElementById('nombres').value.trim();
        if (dni.length !== 8) {
            showAlert('Ingrese un DNI de 8 dígitos.');
            return false;
        }
        if (!nombres) {
            showAlert('El nombre del denunciante es obligatorio.');
            return false;
        }
    } else if (step === 2) {
        const tipo = document.getElementById('id_tipo_denuncia').value;
        const fecha = document.getElementById('fecha_hechos').value;
        const hora = document.getElementById('hora_hechos').value;
        const dir = document.getElementById('direccion_hechos').value.trim();
        const desc = document.getElementById('descripcion_hechos').value.trim();
        const modalidad = document.getElementById('modalidad').value;

        if (!tipo || !fecha || !hora || !dir || !desc || !modalidad) {
            showAlert('Complete todos los campos obligatorios de la denuncia.');
            return false;
        }
    }
    return true;
}

// ==============================
// Búsqueda por DNI
// ==============================
async function buscarPersonaPorDNI(dni) {
    try {
        if (!dni || dni.length !== 8) {
            showAlert('Ingrese un DNI válido (8 dígitos).');
            return;
        }

        const resp = await fetch(`/persona_dni/${dni}/json`);
        const result = await resp.json();

        if (result.status === 1 && result.data) {
            const persona = result.data;

            // 1. Asignar Nombres y Apellidos por separado (según la tabla Persona)
            // NOTA: Usamos 'nombre' del objeto persona para el input 'nombres'
            document.getElementById("nombres").value = persona.nombres || "";
            document.getElementById("ape_paterno").value = persona.ape_paterno || "";
            document.getElementById("ape_materno").value = persona.ape_materno || "";

            // 2. Asignar nuevos campos personales
            if (document.getElementById("fecha_nacimiento")) {
                // Se asume formato 'YYYY-MM-DD' de la API para el input type="date"
                document.getElementById("fecha_nacimiento").value = persona.fecha_nacimiento || "";
            }
            if (document.getElementById("estado_civil")) {
                document.getElementById("estado_civil").value = persona.estado_civil || "";
            }
            if (document.getElementById("ocupacion")) {
                document.getElementById("ocupacion").value = persona.ocupacion || "";
            }

            // 3. Teléfono / Dirección / Correo
            const telInput = document.getElementById("telefono");
            if (telInput) telInput.value = persona.telefono || "";

            const dirInput = document.getElementById("direccion_denunciante");
            // La dirección es obligatoria en la tabla, se debe rellenar si existe.
            if (dirInput) dirInput.value = persona.direccion || ""; 

            const emailInput = document.getElementById("correo");
            if (emailInput) emailInput.value = persona.correo || "";

        } else {
            showAlert(result.message || 'Persona no encontrada. Ingrese los datos manualmente.');
            // No borramos lo escrito, por si el usuario quiere llenarlo a mano
        }
    } catch (err) {
        console.error('Error al buscar persona:', err);
        showAlert('Error al buscar persona. Revise la consola.');
    }
}

// ==============================
// Evidencias
// ==============================
function agregarEvidencia() {
    const tipo = document.getElementById('tipo_evidencia').value;
    const archivoInput = document.getElementById('archivo_evidencia');
    const archivo = archivoInput.files[0];
    const descripcion = document.getElementById('descripcion_evidencia').value.trim();

    if (!tipo || !archivo) {
        showAlert('Seleccione un tipo de evidencia y un archivo.');
        return;
    }

    const tbody = document.getElementById('evidencias-table-body');

    // Creamos fila
    const row = document.createElement('tr');

    // Movemos el input file real dentro de la fila para que se envíe en el POST
    const fileInputInRow = archivoInput;
    fileInputInRow.name = 'archivo_evidencia[]';
    fileInputInRow.style.display = 'none';

    // Creamos un nuevo input "limpio" para futuras evidencias
    const nuevoFileInput = document.createElement('input');
    nuevoFileInput.type = 'file';
    nuevoFileInput.id = 'archivo_evidencia';
    nuevoFileInput.className = 'input';

    const celdaTipo = document.createElement('td');
    celdaTipo.innerHTML = `<input type="hidden" name="tipo_evidencia[]" value="${tipo}">${tipo}`;

    const celdaArchivo = document.createElement('td');
    celdaArchivo.textContent = archivo.name;

    const celdaDesc = document.createElement('td');
    celdaDesc.innerHTML =
        `<input type="hidden" name="descripcion_evidencia[]" value="${descripcion}">
         ${descripcion || '-'}`;

    const celdaAccion = document.createElement('td');
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'button is-secondary';
    btn.textContent = 'Eliminar';
    btn.onclick = () => row.remove();
    celdaAccion.appendChild(btn);

    row.appendChild(celdaTipo);
    row.appendChild(celdaArchivo);
    row.appendChild(celdaDesc);
    row.appendChild(celdaAccion);
    row.appendChild(fileInputInRow);

    tbody.appendChild(row);

    // Reemplazamos el input file del formulario por el nuevo vacío
    archivoInput.parentNode.replaceChild(nuevoFileInput, archivoInput);

    // Limpiamos campos
    document.getElementById('tipo_evidencia').value = '';
    document.getElementById('descripcion_evidencia').value = '';
}

// ==============================
// Eventos iniciales
// ==============================
document.addEventListener('DOMContentLoaded', () => {
    showStep(1);

    const dniInput = document.getElementById('dni');
    const btnBuscarDni = document.getElementById('btn-buscar-dni');

    if (dniInput) {
        dniInput.addEventListener('keydown', e => {
            if (e.key === 'Enter') {
                e.preventDefault();
                buscarPersonaPorDNI(dniInput.value.trim());
            }
        });
    }
    if (btnBuscarDni) {
        btnBuscarDni.addEventListener('click', () => {
            buscarPersonaPorDNI(dniInput.value.trim());
        });
    }

    // Navegación entre pasos
    document.getElementById('btn-next-1')?.addEventListener('click', () => {
        if (validateStep(1)) showStep(2);
    });

    document.getElementById('btn-prev-2')?.addEventListener('click', () => showStep(1));
    document.getElementById('btn-next-2')?.addEventListener('click', () => {
        if (validateStep(2)) showStep(3);
    });

    document.getElementById('btn-prev-3')?.addEventListener('click', () => showStep(2));

    // Evidencias
    document.getElementById('agregar-evidencia-btn')?.addEventListener('click', agregarEvidencia);
});
