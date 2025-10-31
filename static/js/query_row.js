// Al hacer click en una fila, enviamos solo el id al servidor y obtenemos datos reales desde la BD
    document.addEventListener('DOMContentLoaded', function() {
      const rows = document.querySelectorAll('table tbody tr.clickable-row');
      const idInput = document.getElementById('input-id_area');
      const nombreInput = document.getElementById('input-nombre');
      const descripcionInput = document.getElementById('input-descripcion');

      function clearSelection() {
        document.querySelectorAll('table tbody tr.selected').forEach(r => r.classList.remove('selected'));
      }

      rows.forEach(row => {
        row.addEventListener('click',  function() {
          const id = this.dataset.id;
          if (!id) return;

          // Marcar visualmente
          clearSelection();
          this.classList.add('selected');

          // Llamada al endpoint JSON que devuelve el área por id
          fetch(`/area/${id}/json`, { method: 'GET', credentials: 'same-origin' })
            .then(resp => {
              if (!resp.ok) throw new Error('Respuesta del servidor: ' + resp.status);
              return resp.json();
            })
            .then(data => {
              if (data && data.status === 1 && data.data) {
                const area = data.data;
                if (idInput) idInput.value = area.id_area || '';
                if (nombreInput) nombreInput.value = area.nombre || '';
                if (descripcionInput) descripcionInput.value = area.descripcion || '';
                if (nombreInput) nombreInput.focus();
              } else {
                // No encontrado
                if (idInput) idInput.value = id;
                if (nombreInput) nombreInput.value = '';
                if (descripcionInput) descripcionInput.value = '';
                alert(data.message || 'Área no encontrada');
              }
            })
            .catch(err => {
              console.error('Error al obtener área:', err);
              alert('Error al obtener datos del área. Revisa la consola.');
            });
        });
      });
    });