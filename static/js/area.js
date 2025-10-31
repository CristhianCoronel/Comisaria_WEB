document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-area");
  const inputs = form.querySelectorAll("input");
  const btnNuevo = document.getElementById("btnNuevo");
  const btnAgregar = document.getElementById("btnAgregar");
  const btnEditar = document.getElementById("btnEditar");
  const tabla = document.getElementById("tabla-areas");
  const formBuscar = document.getElementById("form-buscar");
  const btnBuscar = document.getElementById("btnBuscar");

  let areaSeleccionadaId = null;

  // --- Estado inicial ---
  deshabilitarCampos();
  btnAgregar.disabled = true;
  btnEditar.disabled = true;

  // --- Funciones auxiliares ---
  function limpiarCampos() {
    form.reset();
    areaSeleccionadaId = null;
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

  function agregarFilaTabla(area) {
    const tbody = tabla.querySelector("tbody");
    const tr = document.createElement("tr");
    tr.dataset.id = area.id_area;
    tr.classList.add("clickable-row");
    tr.innerHTML = `
      <td>${area.id_area}</td>
      <td>${area.nombre}</td>
      <td>${area.descripcion || ""}</td>
    `;
    tbody.appendChild(tr);
    tr.addEventListener("click", () => seleccionarFila(tr));
  }

  function actualizarTabla(lista) {
    const tbody = tabla.querySelector("tbody");
    tbody.innerHTML = "";
    lista.forEach(a => agregarFilaTabla(a));
  }

  async function seleccionarFila(tr) {
    const id = tr.dataset.id;
    if (!id) return;

    tabla.querySelectorAll("tbody tr.selected").forEach(r => r.classList.remove("selected"));
    tr.classList.add("selected");

    try {
      const res = await fetch(`/api/areas/${id}`);
      const result = await res.json();

      if (result.status === 1 && result.data) {
        const area = result.data;
        areaSeleccionadaId = area.id_area;

        form.querySelector("input[name='id_area']").value = area.id_area || "";
        form.querySelector("input[name='nombre']").value = area.nombre || "";
        form.querySelector("input[name='descripcion']").value = area.descripcion || "";

        deshabilitarCampos();
        btnAgregar.disabled = true;
        btnEditar.disabled = false;
      } else {
        mostrarMensaje(result.message || "Área no encontrada", "warning");
        limpiarCampos();
      }
    } catch (err) {
      console.error("Error al obtener área:", err);
      mostrarMensaje("Error al obtener datos del área", "error");
    }
  }

  // Activar selección en filas existentes
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
    if (!data.nombre) {
      mostrarMensaje("El nombre del área es obligatorio", "warning");
      return;
    }

    let url = "/api/areas";
    let method = "POST";

    if (areaSeleccionadaId) {
      url = `/api/areas/${areaSeleccionadaId}`;
      method = "PUT";
    }

    try {
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const result = await res.json();

      if (result.status === 1) {
        const resLista = await fetch("/api/areas");
        const lista = await resLista.json();
        if (lista.status === 1) actualizarTabla(lista.data);

        mostrarMensaje(result.message, "success");
        limpiarCampos();
        deshabilitarCampos();
        btnAgregar.disabled = true;
        btnEditar.disabled = true;
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
    if (!areaSeleccionadaId) return;
    habilitarCampos();
    btnAgregar.disabled = false;
    btnEditar.disabled = true;
  });

  // --- BOTÓN BUSCAR ---
  btnBuscar.addEventListener("click", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(formBuscar).entries());

    try {
      const res = await fetch("/api/areas/buscar", {
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
    