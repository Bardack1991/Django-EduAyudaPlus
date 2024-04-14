document.addEventListener('DOMContentLoaded', function () {
  const servicioSelector = document.querySelector('.form-select[aria-label="selectorServicio"]');
  const divSelectorIdioma = document.getElementById('divSelectorIdioma');

  servicioSelector.addEventListener('change', function () {
    if (this.value === "3") {
      divSelectorIdioma.style.display = 'block';
    } else {
      divSelectorIdioma.style.display = 'none';
    }
  });
});

document.getElementById("texto-a-voz").onclick = function() {
    generateContent("Texto a voz");
  };
  
  document.getElementById("voz-a-texto").onclick = function() {
    generateContent("Voz a texto");
  };
  
  document.getElementById("traduccion-texto").onclick = function() {
    generateContent("Traducción texto");
  };
  
  document.querySelectorAll('.accion-usuario').forEach(item => {
      item.addEventListener('click', function() {
        document.querySelectorAll('.accion-usuario').forEach(innerItem => {
          innerItem.classList.remove('active');
        });
        
        this.classList.add('active');
        
        generateContent(this.textContent);
      });
  });
  
  function generateContent(serviceType) {
      const contenidoDiv = document.getElementById("accion-contenido");
      contenidoDiv.innerHTML = '';
    
      const savedFilesDiv = document.createElement("div");
      savedFilesDiv.className = "list-group mb-3"; 
    
      const files = [
        { name: "Archivo 1", date: "2023-03-24" },
        { name: "Archivo 2", date: "2023-03-23" },
        { name: "Archivo 3", date: "2023-03-22" }
      ];
    
      files.forEach(file => {
        const fileItem = document.createElement("div");
        fileItem.className = "list-group-item d-flex justify-content-between align-items-center";
    
        const fileInfo = document.createElement("div");
        fileInfo.innerHTML = `<strong>${file.name}</strong> - ${file.date}`;
    
        const downloadButton = document.createElement("button");
        downloadButton.className = "btn btn-outline-secondary btn-sm";
        downloadButton.innerHTML = `<i class="bi bi-download"></i> Descargar`;
        downloadButton.type = "button";
    
        fileItem.appendChild(fileInfo);
        fileItem.appendChild(downloadButton);
    
        savedFilesDiv.appendChild(fileItem);
      });
    
      const uploadButtonDiv = document.createElement("div");
      uploadButtonDiv.className = "d-grid gap-2";
    
      const uploadButton = document.createElement("button");
      uploadButton.className = "btn btn-primary w-100";
      uploadButton.textContent = "Subir nuevo archivo";
      uploadButton.type = "button";
      uploadButton.setAttribute("data-bs-toggle", "modal");
      uploadButton.setAttribute("data-bs-target", "#exampleModal");
    
      uploadButtonDiv.appendChild(uploadButton);
    
      contenidoDiv.appendChild(savedFilesDiv);
      contenidoDiv.appendChild(uploadButtonDiv);
    }
  