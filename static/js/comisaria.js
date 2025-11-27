// RELLENA DATOS EN LOS CAMPOS
document.querySelectorAll("#tabla-formulario tbody tr").forEach(fila => {
    fila.addEventListener("click", async () => {

        const id = Number(fila.cells[0].innerText.trim());
        console.log("Comisaría seleccionada:", id);

        try {
            const resp = await fetch(`/comisaria/${id}/json`);
            const result = await resp.json();

            if (resp.ok && result.status === 1) {
                const c = result.data;

                const form = document.getElementById("form-comisaria");

                form.id_comisaria.value = c.id_comisaria || "";
                form.nombre.value = c.nombre || "";
                form.telefono.value = c.telefono || "";
                form.direccion.value = c.direccion || "";
                form.ubigeo.value = c.ubigeo || "";

            } else {
                alert(result.message || "No se pudo cargar los datos.");
            }

        } catch (error) {
            console.error(error);
            alert("Error al comunicarse con el servidor.");
        }

    });
});

// ELIMINA VALOR DEL ID PARA REGISTRAR
document.getElementById("btnNuevo").addEventListener("click", () => {
    const form = document.getElementById("form-comisaria");
    form.reset();
    form.id_comisaria.value = "";  // importante
});

// FUNCIÓN DE VALIDAR CAMPOS
function validarCampos() {
    const campos = document.querySelectorAll(".validar");
    let valido = true;
    console.log("Valida los campos");
    campos.forEach(campo => {
        if (campo.value.trim() === "") {
            campo.classList.add("error");
            valido = false;
            console.log("Se encontro un error");
        } else {
            campo.classList.remove("error");
            console.log("Removiendo el error");
        }
    });

    return valido; // true = todo bien | false = falta algo
}

// REGISTRAR O ACTUALIZAR COMISARIA
document.getElementById("btnGuardar").addEventListener("click", (e) => {
    e.preventDefault();
    
    const form = document.getElementById("form-comisaria");
    const id = form.id_comisaria.value.trim();
    if (validarCampos()) {
        // Si tiene ID → actualizar
        if (id !== "") {
            console.log("Vamos a actualizar");
            form.action = "/comisaria/actualizar";
        } 
        else {
            console.log("Vamos a registrar");
            form.action = "/comisaria/registrar";
        }

        form.method = "POST";
        form.submit();
        console.log("Se hizo submit");
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

// BUSCAR COMISARIA POR NOMBRE Y UBIGEO
document.getElementById("btnBuscar").addEventListener("click", () => {
    const form = document.getElementById("form-buscar");

    const nombre = form.b_nombre.value.trim();
    const ubigeo = form.b_ubigeo.value.trim();

    // Construir URL (si está vacío, enviar _ para evitar que falle la ruta)
    const url = `/comisaria/buscar/${nombre || "_"}\/${ubigeo || "_"}`;

    // Redirigir
    window.location.href = url;
});