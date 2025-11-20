// ===========================
//  FORMULARIOS.JS – CONTROL GENERAL
// ===========================

// ---- Obtener elementos ----
const inputs = document.querySelectorAll('form input');
const selects = document.querySelectorAll('form select');
const textsA = document.querySelectorAll('form textarea');
const btnNuevo = document.getElementById('btnNuevo');
const btnGuardar = document.getElementById('btnGuardar');
const btnEditar = document.getElementById('btnEditar');
const tabla = document.getElementById('tabla-formulario');

// Estado actual
let modo = "ninguno"; // "nuevo", "editar", "ninguno"



// ===========================
//  FUNCIONES DE APOYO
// ===========================

function deshabilitarCampos() {
    inputs.forEach(i => i.disabled = true);
    selects.forEach(i => i.disabled = true);
    textsA.forEach(i => i.disabled = true);
}

function habilitarCampos() {
    inputs.forEach(i => i.disabled = false);
    selects.forEach(i => i.disabled = false);
    textsA.forEach(i => i.disabled = false);
}

function limpiarCampos() {
    inputs.forEach(i => i.value = "");
    selects.forEach(i => i.selectedIndex = 0);
    textsA.forEach(i => i.value = "");
}

function deshabilitarTabla() {
    tabla.classList.add("disabled-table"); 
    // Opcional: impedir clics
    tabla.style.pointerEvents = "none";
    tabla.style.opacity = "0.6";
}

function habilitarTabla() {
    tabla.classList.remove("disabled-table");
    tabla.style.pointerEvents = "auto";
    tabla.style.opacity = "1";
}

function restaurarBotones() {
    btnNuevo.textContent = "Nuevo";
    btnEditar.textContent = "Editar";
}



// ===========================
//  ESTADO INICIAL
// ===========================

window.addEventListener("DOMContentLoaded", () => {
    deshabilitarCampos();
    btnGuardar.disabled = true;
    btnEditar.disabled = true;
    btnNuevo.disabled = false;
    habilitarTabla();
    modo = "ninguno";
});



// ===========================
//  BOTÓN NUEVO
// ===========================

btnNuevo.addEventListener("click", () => {

    if (btnNuevo.textContent === "Nuevo") {
        // Activar modo nuevo
        modo = "nuevo";
        btnNuevo.textContent = "Cancelar";

        habilitarCampos();
        limpiarCampos();

        btnGuardar.disabled = false;
        btnEditar.disabled = true;

        deshabilitarTabla();
    }
    else {
        // CANCELAR desde NUEVO
        modo = "ninguno";
        btnNuevo.textContent = "Nuevo";

        deshabilitarCampos();
        limpiarCampos();

        btnGuardar.disabled = true;
        btnEditar.disabled = true;

        habilitarTabla();
    }
});



// ===========================
//  BOTÓN EDITAR
// ===========================

btnEditar.addEventListener("click", () => {

    if (btnEditar.textContent === "Editar") {
        // Activar modo editar
        modo = "editar";
        btnEditar.textContent = "Cancelar";

        habilitarCampos();
        btnGuardar.disabled = false;

        deshabilitarTabla();
    }
    else {
        // CANCELAR desde EDITAR
        modo = "ninguno";
        btnEditar.textContent = "Editar";

        deshabilitarCampos();

        btnGuardar.disabled = true;
        btnEditar.disabled = true;

        habilitarTabla();
    }
});



// ===========================
//  BOTÓN GUARDAR
// ===========================

btnGuardar.addEventListener("click", () => {
    // Aquí NO guardamos datos (eso va en persona.js o comisaria.js)
    // Solo manejamos estado visual

    modo = "ninguno";

    deshabilitarCampos();
    limpiarCampos();
    habilitarTabla();

    btnGuardar.disabled = true;
    btnEditar.disabled = true;

    restaurarBotones();
});



// ===========================
//  TABLA – Selección de fila
// ===========================

tabla.addEventListener("click", (e) => {
    const fila = e.target.closest("tr");
    if (!fila) return;

    // Habilitar editar al seleccionar
    btnEditar.disabled = false;
});
