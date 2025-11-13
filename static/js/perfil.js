document.addEventListener("DOMContentLoaded", () => {
  const btnEditar = document.getElementById("btnEditar");
  const btnGuardar = document.getElementById("btnGuardar");
  const btnCancelar = document.getElementById("btnCancelar");
  const acciones = document.getElementById("acciones");
  const accionesEdicion = document.getElementById("accionesEdicion");

  const inputs = document.querySelectorAll("input[type='text']:not([disabled][id='codigo'])");

  let originalData = {};

  const guardarDatosOriginales = () => {
    inputs.forEach(input => {
      originalData[input.id] = input.value;
    });
  };

  const habilitarEdicion = (habilitar) => {
    inputs.forEach(input => {
      if (input.id !== "codigo" && input.id !== "comisaria" && input.id !== "rango" && input.id !== "rol") {
        input.disabled = !habilitar;
        input.style.background = habilitar ? "white" : "#f3f4f6";
      }
    });
  };

  btnEditar.addEventListener("click", () => {
    guardarDatosOriginales();
    btnEditar.classList.add("hidden");
    accionesEdicion.classList.remove("hidden");
    habilitarEdicion(true);
  });

  btnCancelar.addEventListener("click", () => {
    for (let key in originalData) {
      document.getElementById(key).value = originalData[key];
    }
    btnEditar.classList.remove("hidden");
    accionesEdicion.classList.add("hidden");
    habilitarEdicion(false);
  });

  btnGuardar.addEventListener("click", () => {
    const updatedData = {};
    inputs.forEach(input => updatedData[input.id] = input.value);

    console.log("Guardando datos:", updatedData);

    document.getElementById("nombreCompleto").textContent =
      `${updatedData.nombres} ${updatedData.ape_paterno} ${updatedData.ape_materno}`;

    btnEditar.classList.remove("hidden");
    accionesEdicion.classList.add("hidden");
    habilitarEdicion(false);
  });
});
