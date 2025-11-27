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
                form.comisaria.value = p.id_comisaria || "";
                form.tipo_usuario.value = p.tipo_usuario || "";
                form.estado.value = p.estado || "";
                form.rango.value = p.id_rango || "";
                form.rol.value = p.id_rol || "";

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
