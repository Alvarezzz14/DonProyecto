function filtrarTabla() {
    const input = document.getElementById('filtroEdad');
    const filter = input.value.toUpperCase();
    const table = document.getElementById('tablaPersonas');
    const rows = table.getElementsByTagName('tr');
  
    for (let i = 1; i < rows.length; i++) {
      let shouldShow = false;
  
      const cells = rows[i].getElementsByTagName('td');
      for (let j = 0; j < cells.length - 1; j++) {
        const cellText = cells[j].innerText || cells[j].textContent;
        if (cellText.toUpperCase().includes(filter)) {
          shouldShow = true;
          break;
        }
      }
  
      if (shouldShow || filter === '') {
        rows[i].style.display = '';
      } else {
        rows[i].style.display = 'none';
      }
    }
  }
  
  /*let isEditing = false;
  
  function editarFila(button) {
    const row = button.parentNode.parentNode;
    const cells = row.getElementsByTagName('td');
  
    for (let i = 0; i < cells.length - 1; i++) {
      cells[i].contentEditable = true;
      cells[i].style.backgroundColor = '#f3f3f3';
    }
  
    isEditing = true;
  }
  
  function guardarEdicion(button) {
    if (!isEditing) return;
  
    const row = button.parentNode.parentNode;
    const cells = row.getElementsByTagName('td');
  
    for (let i = 0; i < cells.length - 1; i++) {
      cells[i].contentEditable = false;
      cells[i].style.backgroundColor = 'white';
    }
  
    isEditing = false;
  }
  
  function agregarFila() {
    const table = document.getElementById('tablaPersonas').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow(table.rows.length);
  
    const cell1 = newRow.insertCell(0);
    const cell2 = newRow.insertCell(1);
    const cell3 = newRow.insertCell(2);
    const cell4 = newRow.insertCell(3);
    const cell5 = newRow.insertCell(4);
  
    cell1.innerHTML = 'NuevoNombre';
    cell2.innerHTML = 'NuevaEdad';
    cell3.innerHTML = 'NuevaCiudad';
    cell4.innerHTML = 'NuevaProfesión';
    cell5.innerHTML = '<button onclick="editarFila(this)">Editar</button><button onclick="guardarEdicion(this)">Guardar</button>';
  } */
  
  function eliminarFila(index) {
    const table = document.getElementById('tablaPersonas').getElementsByTagName('tbody')[0];
    if (table.rows.length > 0) {
      table.deleteRow(index);
    }
  }

  
