// RELLENAR DATOS EN LOS CAMPOS
document.querySelectorAll("#tabla-formulario tbody tr").forEach(fila => {
    fila.addEventListener("click", async () => {

        const id = Number(fila.cells[0].innerText.trim());
        console.log("Persona seleccionada:", id);

        try {
            const resp = await fetch(`/persona/${id}/json`);
            const result = await resp.json();

            if (resp.ok && result.status === 1) {
                const p = result.data;

                const form = document.getElementById("form-persona");

                form.id_persona.value = p.id_persona || "";
                form.dni.value = p.dni || "";
                form.nombres.value = p.nombres || "";
                form.ape_paterno.value = p.ape_paterno || "";
                form.ape_materno.value = p.ape_materno || "";
                form.telefono.value = p.telefono || "";
                form.estado_civil.querySelected = p.estado_civil || "";
                form.ocupacion.value = p.ocupacion || "";
                form.direccion.value = p.direccion || "";
                form.ubigeo.value = p.ubigeo || "";

                // 👉 Fecha: convertir a yyyy-mm-dd solo si existe
                if (p.fecha_nacimiento) {
                    form.fecha_nacimiento.value = p.fecha_nacimiento.substring(0, 10);
                } else {
                    form.fecha_nacimiento.value = ""; 
                }

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
    const form = document.getElementById("form-persona");
    form.reset();
    form.id_persona.value = "";  // importante
});
// FUNCIÓN DE VALIDAR CAMPOS
function validarCampos() {
    const campos = document.querySelectorAll(".validar");
    let valido = true;

    campos.forEach(campo => {
        if (campo.value.trim() === "") {
            campo.classList.add("error");
            valido = false;
        } else {
            campo.classList.remove("error");
        }
    });

    return valido; // true = todo bien | false = falta algo
}
// REGISTRAR O ACTUALIZAR CIUDADANO
document.getElementById("btnGuardar").addEventListener("click", () => {
    const form = document.getElementById("form-persona");

    const id = form.id_persona.value.trim();
    if (validarCampos()) {
        // Si tiene ID → actualizar
        if (id !== "") {
            form.action = "/ciudadano/actualizar";
        } 
        // Si NO tiene ID → registrar
        else {
            form.action = "/ciudadano/registrar";
        }

        form.method = "POST";
        form.submit();
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
    const url = `/ciudadano/buscar/${dni || "_"}\/${nombre || "_"}`;

    // Redirigir
    window.location.href = url;
});
