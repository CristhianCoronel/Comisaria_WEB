// RELLENAR DATOS EN LOS CAMPOS
document.querySelectorAll("#tabla-formulario tbody tr").forEach(fila => {
    fila.addEventListener("click", async () => {

        const id = Number(fila.cells[0].innerText.trim());
        console.log("Usuario seleccionada:", id);

        try {
            const resp = await fetch(`/personal/${id}/json`);
            const result = await resp.json();
            if (resp.ok && result.status === 1) {
                const p = result.data;
                const form = document.getElementById("form-usuario");

                form.id_usuario.value = p.id_usuario || "";
                form.dni.value = p.dni || "";
                form.nombres.value = p.nombres || "";
                form.ape_paterno.value = p.ape_paterno || "";
                form.ape_materno.value = p.ape_materno || "";
                form.id_comisaria.value = p.id_comisaria || "";
                form.tipo_usuario.value = p.tipo_usuario || "";
                form.estado.value = p.estado || "";
                form.id_rango.value = p.id_rango || "";
                form.id_rol.value = p.id_rol || "";
                
            } else {
                alert(result.message || "No se pudo cargar los datos.");
            }

        } catch (error) {
            console.error(error);
            alert("Error al comunicarse con el servidor.");
        }

    });
});

// ELIMINAR VALOR DEL ID PARA REGISTRAR
document.getElementById("btnNuevo").addEventListener("click", () => {
    const form = document.getElementById("form-usuario");
    form.reset();
    form.id_usuario.value = "";  // importante
});

// FUNCIÓN DE VALIDAR CAMPOS
function validarCampos() {
    const codigo = document.querySelector('[name="codigo_usuario"]');
    const id_usuario = document.querySelector('[name="id_usuario"]');
    let valido = true;

    if (!codigo || !id_usuario) {
        console.error("❌ No se encontraron los campos en el DOM");
        return false; // Evita error al intentar acceder a .value
    }

    // Si id_usuario está vacío → desactivar codigo
    if (id_usuario.value.trim() !== "") {
        codigo.classList.remove("validar");
    }

    // Obtener todos los campos que deben validarse
    const campos = document.querySelectorAll(".validar");

    campos.forEach(campo => {
        if (campo.value.trim() == "") {
            campo.classList.add("error");
            valido = false;
        } else {
            campo.classList.remove("error");
        }
    });

    // Reagregar validación a codigo si id_usuario estaba vacío
    if (id_usuario.value.trim() !== "") {
        codigo.classList.add("validar");
    }

    return valido; 
}

// DESHABILITAR CODIGO DE USUARIO AL EDITAR
document.getElementById("btnEditar").addEventListener("click", function () {
    const codigo = document.querySelector('[name="codigo_usuario"]');
    if (codigo) {
        codigo.disabled = true;
    } else {
        console.error("Input con name='codigo_usuario' no encontrado");
    }
});

// REGISTRAR O ACTUALIZAR CIUDADANO
document.getElementById("btnGuardar").addEventListener("click", (e) => {
    e.preventDefault(); // Evita que el formulario se envíe automáticamente

    const form = document.getElementById("form-usuario");
    const id = form.id_usuario.value.trim();

    if (validarCampos()) {
        // Definir la acción según si es actualizar o registrar
        if (id !== "") {
            form.action = "/personal/actualizar";
        } else {
            form.action = "/personal/registrar";
        }

        form.method = "POST";
        form.submit();

        modo = "ninguno";

        deshabilitarCampos();
        limpiarCampos();
        habilitarTabla();

        btnGuardar.disabled = true;
        btnEditar.disabled = true;

        restaurarBotones();

    } else {
        alert("Completa todos los campos obligatorios.");
    }
});

// BUSCAR PERSONA POR NOMBRE Y DNI
document.getElementById("btnBuscar").addEventListener("click", () => {
    const form = document.getElementById("form-buscar");

    const nombre = form.b_nombre.value.trim();
    const dni = form.b_dni.value.trim();

    // Construir URL (si está vacío, enviar _ para evitar que falle la ruta)
    const url = `/personal/buscar/${nombre || "_"}\/${dni || "_"}`;

    // Redirigir
    window.location.href = url;
});

/* ============================
   ABRIR MODAL
   ============================ */
const modal = document.getElementById("modal");
const closeModal = document.getElementById("closeModal");

const code1 = document.getElementById("code1");
const code2 = document.getElementById("code2");
const errorMsg = document.getElementById("errorMsg");
const form = document.getElementById("codeForm");

const inputID = document.getElementById("id_usuario");


function abrirModal() {
    code1.value = "";
    code2.value = "";
    errorMsg.textContent = "";
    modal.style.display = "flex";
}

closeModal.onclick = () => modal.style.display = "none";
window.onclick = (e) => { if (e.target === modal) modal.style.display = "none"; };

/* ============================
   VALIDACIÓN
   ============================ */
function validar() {
    const val1 = code1.value;
    const val2 = code2.value;

    if (val1.includes("'") || val1.includes('"') || val2.includes("'") || val2.includes('"')) {
        errorMsg.textContent = "No se permiten comillas simples ni dobles.";
        errorMsg.style.display = "block"; // Mostrar solo si hay error
        return false;
    }

    if (val1.length < 6) {
        errorMsg.textContent = "El código debe tener al menos 6 caracteres.";
        errorMsg.style.display = "block";
        return false;
    }

    if (val1 !== val2) {
        errorMsg.textContent = "Los códigos no coinciden.";
        errorMsg.style.display = "block";
        return false;
    }

    errorMsg.textContent = "";
    errorMsg.style.display = "none"; // Ocultar si no hay error
    return true;
}

code1.addEventListener("input", validar);
code2.addEventListener("input", validar);

form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!validar()) return;

    form.action = `/usuario/codigo/${inputID.value}`;   // ruta correcta
    form.method = "POST";                               // enviar por POST
    form.submit();                                      // enviar formulario
});
