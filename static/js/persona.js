document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-persona");
  const inputs = form.querySelectorAll("input");
  const btnNuevo = document.getElementById("btnNuevo");
  const btnAgregar = document.getElementById("btnAgregar");
  const btnEditar = document.getElementById("btnEditar");
  const formBuscar = document.getElementById("form-buscar");
  const btnBuscar = document.getElementById("btnBuscar");

  // --- Estado inicial ---
  deshabilitarCampos();
  btnAgregar.disabled = true;
  btnEditar.disabled = true;

  // --- BOTÓN NUEVO ---
  btnNuevo.addEventListener("click", () => {
    limpiarCampos();
    habilitarCampos();
    btnAgregar.disabled = false;
    btnEditar.disabled = true;
  });

  // --- BOTÓN AGREGAR ---
  btnAgregar.addEventListener("click", async () => {
    const data = Object.fromEntries(new FormData(form).entries());

    try {
      const res = await fetch("/api/personas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await res.json();

      if (result.status === 1) {
        agregarFilaTabla(result.data);
        mostrarMensaje(result.message, "success");
        limpiarCampos();
        deshabilitarCampos();
        btnAgregar.disabled = true;
      } else {
        mostrarMensaje(result.message, "warning");
      }
    } catch (error) {
      mostrarMensaje("Error de conexión con el servidor", "error");
      console.error("Error:", error);
    }
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

  // --- FUNCIONES AUXILIARES ---
  function limpiarCampos() {
    form.reset();
  }

  function habilitarCampos() {
    inputs.forEach(i => i.disabled = false);
  }

  function deshabilitarCampos() {
    inputs.forEach(i => i.disabled = true);
  }

  function agregarFilaTabla(persona) {
    const tbody = document.querySelector("#tabla-personas tbody");
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${persona.id_persona}</td>
      <td>${persona.dni}</td>
      <td>${persona.nombres}</td>
      <td>${persona.apellidos}</td>
      <td>${persona.fecha_nacimiento || ""}</td>
      <td>${persona.telefono || ""}</td>
      <td>${persona.direccion || ""}</td>
    `;
    tbody.appendChild(tr);
  }

  function actualizarTabla(lista) {
    const tbody = document.querySelector("#tabla-personas tbody");
    tbody.innerHTML = "";
    lista.forEach(p => agregarFilaTabla(p));
  }

  // --- SWEETALERT2: MENSAJES BONITOS ---
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
});
