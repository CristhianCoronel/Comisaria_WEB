document.addEventListener("DOMContentLoaded", async function() {
  const rbUbigeo = document.querySelectorAll('input[name="rb_ubigeo"]');
  const divSelect = document.getElementById("divUbigeoSelect");
  const divDesconocido = document.getElementById("divUbigeoDesconocido");
  const lblUbigeo = document.getElementById("lbl_ubigeo");
  const txtUbigeoFinal = document.getElementById("txt_ubigeo_final");
  const cbDepartamento = document.getElementById("cb_departamento");
  const cbProvincia = document.getElementById("cb_provincia");
  const cbDistrito = document.getElementById("cb_distrito");

  // --- Alternar entre modos ---
  rbUbigeo.forEach(r => {
    r.addEventListener("change", () => {
      if (r.value === "no_se" && r.checked) {
        divSelect.style.display = "none";
        divDesconocido.style.display = "block";
        cargarDepartamentos();
      } else if (r.value === "conocido" && r.checked) {
        divSelect.style.display = "block";
        divDesconocido.style.display = "none";
      }
    });
  });

  // --- Cargar departamentos ---
  async function cargarDepartamentos() {
    try {
      const res = await fetch("/api_obtener_departamentos");
      const data = await res.json();
      if (data.status === 1) {
        cbDepartamento.innerHTML = '<option value="">Seleccione departamento</option>';
        data.data.forEach(dep => {
          cbDepartamento.innerHTML += `<option value="${dep.codigo}">${dep.nombre}</option>`;
        });
      }
    } catch (err) {
      console.error("Error al cargar departamentos:", err);
    }
  }

  // --- Cambiar departamento ---
  cbDepartamento.addEventListener("change", async () => {
    const codDep = cbDepartamento.value;
    cbProvincia.innerHTML = '<option value="">Seleccione provincia</option>';
    cbDistrito.innerHTML = '<option value="">Seleccione distrito</option>';
    lblUbigeo.textContent = "Ubigeo: —";
    txtUbigeoFinal.value = "";
    if (!codDep) return;

    try {
      const res = await fetch(`/api_obtener_provinciasxdepartamento/${codDep}`);
      const data = await res.json();
      if (data.status === 1) {
        data.data.forEach(prov => {
          cbProvincia.innerHTML += `<option value="${prov.codigo}">${prov.nombre}</option>`;
        });
      }
    } catch (err) {
      console.error("Error al cargar provincias:", err);
    }
  });

  // --- Cambiar provincia ---
  cbProvincia.addEventListener("change", async () => {
    const codProv = cbProvincia.value;
    cbDistrito.innerHTML = '<option value="">Seleccione distrito</option>';
    lblUbigeo.textContent = "Ubigeo: —";
    txtUbigeoFinal.value = "";
    if (!codProv) return;

    try {
      const res = await fetch(`/api_obtener_distritosxprovincia/${codProv}`);
      const data = await res.json();
      if (data.status === 1) {
        data.data.forEach(dist => {
          cbDistrito.innerHTML += `<option value="${dist.codigo}">${dist.nombre}</option>`;
        });
      }
    } catch (err) {
      console.error("Error al cargar distritos:", err);
    }
  });

  // --- Cambiar distrito ---
  cbDistrito.addEventListener("change", async () => {
    const codDist = cbDistrito.value;
    if (!codDist) return;

    try {
      const res = await fetch(`/api_obtener_ubigeoxdistrito/${codDist}`);
      const data = await res.json();
      if (data.status === 1 && data.data.length > 0) {
        const ubigeo = data.data[0].codigo;
        lblUbigeo.textContent = `Ubigeo: ${ubigeo}`;
        txtUbigeoFinal.value = ubigeo;
      }
    } catch (err) {
      console.error("Error al obtener ubigeo:", err);
    }
  });
});
