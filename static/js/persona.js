document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-persona");
  const inputs = form.querySelectorAll("input");
  const btnNuevo = document.getElementById("btnNuevo");
  const btnAgregar = document.getElementById("btnAgregar");
  const btnEditar = document.getElementById("btnEditar");
  const formBuscar = document.getElementById("form-buscar");
  const btnBuscar = document.getElementById("btnBuscar");
  const tabla = document.getElementById("tabla-personas");

  let personaSeleccionadaId = null;

  // --- Estado inicial ---
  deshabilitarCampos();
  btnAgregar.disabled = true;
  btnEditar.disabled = true;

  // --- Funciones auxiliares ---
  function limpiarCampos() {
    form.reset();
    personaSeleccionadaId = null;
  }

  function habilitarCampos() {
    inputs.forEach(i => i.disabled = false);
  }

  function deshabilitarCampos() {
    inputs.forEach(i => i.disabled = true);
  }

  function mostrarMensaje(msg, tipo = "success") {
    Swal.fire({
      icon: tipo === "success" ? "success" :
            tipo === "warning" ? "warning" :
            tipo === "error" ? "error" : "info",
      title: msg,
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 2500,
      timerProgressBar: true,
    });
  }

  function agregarFilaTabla(persona) {
    const tbody = tabla.querySelector("tbody");
    const tr = document.createElement("tr");
    tr.dataset.id = persona.id_persona;
    tr.innerHTML = `
      <td>${persona.id_persona}</td>
      <td>${persona.dni}</td>
      <td>${persona.nombres}</td>
      <td>${persona.ape_paterno}</td>
      <td>${persona.ape_materno}</td>
      <td>${persona.fecha_nacimiento || ""}</td>
      <td>${persona.telefono || ""}</td>
      <td>${persona.direccion || ""}</td>
    `;
    tr.classList.add("clickable-row");
    tbody.appendChild(tr);

    // Activar selección al hacer click
    tr.addEventListener("click", () => seleccionarFila(tr));
  }

  function actualizarTabla(lista) {
    const tbody = tabla.querySelector("tbody");
    tbody.innerHTML = "";
    lista.forEach(p => agregarFilaTabla(p));
  }

  async function seleccionarFila(tr) {
    const id = tr.dataset.id;
    if (!id) return;

    // Limpiar selección previa
    tabla.querySelectorAll("tbody tr.selected").forEach(r => r.classList.remove("selected"));
    tr.classList.add("selected");

    try {
      const res = await fetch(`/persona/${id}/json`, { method: "GET" }); // Ajusta la URL a tu endpoint real
      const result = await res.json();

      if (result.status === 1 && result.data) {
        const persona = result.data;
        personaSeleccionadaId = persona.id_persona;

        // Llenar inputs
        form.querySelector("input[name='dni']").value = persona.dni || "";
        form.querySelector("input[name='nombres']").value = persona.nombres || "";
        form.querySelector("input[name='ape_paterno']").value = persona.ape_paterno || "";
        form.querySelector("input[name='ape_materno']").value = persona.ape_materno || "";
        form.querySelector("input[name='fecha_nacimiento']").value = persona.fecha_nacimiento || "";
        form.querySelector("input[name='telefono']").value = persona.telefono || "";
        form.querySelector("input[name='direccion']").value = persona.direccion || "";
        form.querySelector("input[name='ubigeo']").value = persona.ubigeo || "";

        // Bloquear inputs y habilitar solo Editar
        deshabilitarCampos();
        btnAgregar.disabled = true;
        btnEditar.disabled = false;
        btnNuevo.disabled = false;
      } else {
        mostrarMensaje(result.message || "Persona no encontrada", "warning");
        limpiarCampos();
      }
    } catch (err) {
      console.error("Error al obtener persona:", err);
      mostrarMensaje("Error al obtener datos de la persona", "error");
    }
  }

  // --- Activar selección en filas existentes ---
  tabla.querySelectorAll("tbody tr").forEach(tr => {
    tr.classList.add("clickable-row");
    tr.addEventListener("click", () => seleccionarFila(tr));
  });

  // --- BOTÓN NUEVO ---
  btnNuevo.addEventListener("click", () => {
    limpiarCampos();
    habilitarCampos();
    btnAgregar.disabled = false;
    btnEditar.disabled = true;
    tabla.querySelectorAll("tbody tr.selected").forEach(r => r.classList.remove("selected"));
  });

  // --- BOTÓN AGREGAR / GUARDAR ---
  btnAgregar.addEventListener("click", async () => {
    const data = Object.fromEntries(new FormData(form).entries());

    let url = "/api/personas";
    let method = "POST";
    if (!data.dni || !data.nombres || !data.ape_paterno) {
      mostrarMensaje("Completa los campos obligatorios (*)", "warning");
      return;
    }
    if (personaSeleccionadaId) {
      // Si hay una persona seleccionada, usamos PUT para actualizar
      url = `/api/personas/${personaSeleccionadaId}`;
      method = "PUT";
    }

    try {
      const res = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await res.json();

      if (result.status === 1) {
        // Recargar lista completa desde el servidor
        const resLista = await fetch("/api/personas", { method: "GET" });
        const lista = await resLista.json();

        if (lista.status === 1) {
          actualizarTabla(lista.data);
        }

        mostrarMensaje(result.message, "success");
        limpiarCampos();
        deshabilitarCampos();
        btnAgregar.disabled = true;
        btnEditar.disabled = true;
        personaSeleccionadaId = null;
      } else {
        mostrarMensaje(result.message, "warning");
      }
    } catch (error) {
      mostrarMensaje("Error de conexión con el servidor", "error");
      console.error("Error:", error);
    }
  });


  // --- BOTÓN EDITAR ---
  btnEditar.addEventListener("click", () => {
    if (!personaSeleccionadaId) return;
    habilitarCampos();
    btnAgregar.disabled = false;
    btnEditar.disabled = true;
  });

  // --- BOTÓN BUSCAR ---
  btnBuscar.addEventListener("click", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(formBuscar).entries());

    try {
      const res = await fetch("/api/personas/buscar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await res.json();
      if (result.status === 1) {
        actualizarTabla(result.data);
        mostrarMensaje(`${result.data.length} resultado(s) encontrado(s)`, "info");
      } else {
        mostrarMensaje(result.message, "warning");
      }
    } catch (error) {
      mostrarMensaje("Error de conexión con el servidor", "error");
      console.error("Error:", error);
    }
  });
});
