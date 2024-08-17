async function delete_thumbs(button) {

    const imageId = button.getAttribute('data-id');
            
        if (!imageId) {
            console.error('ID de imagen no encontrado.');
            return;
        }

        try {
            const response = await fetch(`/delete_image_report/${imageId}/`, {
                method: 'DELETE', // Método DELETE para eliminar
                headers: {
                    'Content-Type': 'application/json',
                    
                }
            });
            if (response.ok) {
                // Eliminar el elemento del DOM si la eliminación en el servidor fue exitosa
                button.parentNode.remove();
            } else {
                console.error('Error al eliminar la imagen:', response.statusText);
            }
        } catch (error) {
            console.error('Error en la solicitud:', error);
        }
    

   

};

function thumbs_process(){

        const uploadForm = document.getElementById('uploadForm');
        const fileInput = document.getElementById('files');
        const imagePreview = document.getElementById('imagePreview');

    // Manejar la selección de archivos para previsualización
    //fileInput.addEventListener('change', function() {
        
        if (fileInput.files.length > 9) { // Cambia el número a tu límite deseado
            alert("Solo puedes subir un máximo de 9 imágenes.");
            input.value = ''; // Borra la selección de archivos
        }

        const files = fileInput.files;
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (!file.type.startsWith('image/')) { continue; }

            const reader = new FileReader();
            reader.onload = function(e) {
                const thumbnail = document.createElement('div');
                thumbnail.name = "thumbs"
                thumbnail.classList.add('col-sm-3', 'mb-3');

                const img = document.createElement('img');
                img.src = e.target.result;
                img.classList.add('img-thumbnail', 'img-fluid');
                img.style.maxWidth = '100%';

                const caption = document.createElement('div');
                caption.classList.add('text-end');

                const deleteBtn = document.createElement('button');
                deleteBtn.type = 'button';
                deleteBtn.classList.add('btn', 'btn-close', 'btn-sm');

                deleteBtn.addEventListener('click', function delete_thumbs() {
                    thumbnail.parentNode.removeChild(thumbnail);
                });

                caption.appendChild(deleteBtn);
                thumbnail.appendChild(caption);
                thumbnail.appendChild(img);
                
                imagePreview.appendChild(thumbnail);
            };
            reader.readAsDataURL(file);
        }
    //});

    // Prevenir envío del formulario al hacer clic en Delete
    imagePreview.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('delete-btn')) {
            e.preventDefault();
        }
    });


}



function close_flashed_msg(){
    // Find the closest parent alert div element to the clicked button
    var alertDiv = event.target.closest('.alert');

    // Check if the alert div was found
    if (alertDiv) {
        // Remove the alert div from the DOM
        alertDiv.remove();
    }
}


// add users in forms

function add_workers(users){

    var selectedUsersInputs = {};
    var selectCounter = 0;

    document.getElementById("add-worker").addEventListener("click", function(){

        

        var container = document.getElementById("team-container");
        var workerDiv = document.createElement("div");
        workerDiv.className = "worker-select mt-2 container row justify-content-center";

        var workerSelect = document.createElement("select");
        workerSelect.className = "form-select col";
        workerSelect.name = "team[]";
        selectCounter += 1;
        workerSelect.id = `select_id_${selectCounter}`

        var defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.text = "Seleccione un trabajador"
        workerSelect.appendChild(defaultOption);

        var resposibleSelect = document.getElementById("responsible_id");
        var responsible_id = parseInt(resposibleSelect.value);

        users.forEach(function(user) {
            if (!Object.values(selectedUsersInputs).includes(user.id.toString()) && user.id !== responsible_id){
                var option = document.createElement("option");
                option.value = user.id;
                option.textContent = user.name;
                workerSelect.appendChild(option);
           }
        }
        );
        if(!Object.values(selectedUsersInputs).includes("external")) {
            console.log("ingresa a externla if")
            var externalOption = document.createElement('option');
            externalOption.value = "external";
            externalOption.text = "Trabajador externo";
            workerSelect.appendChild(externalOption);
            
        }

        workerDiv.appendChild(workerSelect);

        var removeButton = document.createElement("button");
        removeButton.className = "btn btn-close col-2 align-self-center";
        removeButton.onclick = function() {
            container.removeChild(workerDiv);
            
            delete selectedUsersInputs[workerSelect.id]
            updateOptions();
        };

        workerDiv.appendChild(removeButton)
        container.appendChild(workerDiv)

        workerSelect.addEventListener("change", function(){
            var selectedValue = workerSelect.value;
            
            console.log("selected option", selectedValue)
            if(selectedValue === "external"){
                var externalInput = document.createElement("input");
                externalInput.type = "number";
                externalInput.name = "n_external";
                externalInput.id = "n_external";
                externalInput.className = "form-control";
                externalInput.placeholder = "# trabajadores externos";
                workerDiv.appendChild(externalInput);
            }

            selectedUsersInputs[workerSelect.id] = selectedValue;
            console.log("selected row option", selectedUsersInputs)
            
            updateOptions();
        });
    });

    document.getElementById("responsible_id").addEventListener("change", updateOptions);
    
    document.querySelectorAll("select[name='team[]']").forEach(function(select) {
        select.addEventListener("click", updateOptions);
    });
    
    function updateOptions() {
        console.log("entra a updateOptions")
        console.log("selected inputs: ", selectedUsersInputs)
        var selects = document.querySelectorAll("select[name='team[]']");
        
        var resposibleSelect =  document.getElementById("responsible_id");
    
        var responsible_id = parseInt(resposibleSelect.value);
        
        selects.forEach(function(select){
            var currentValue = select.value;
            selectedUsersInputs[select.id] = currentValue;
            
            select.innerHTML = "";
            
            if( parseInt(currentValue) === responsible_id ){
                var defaultOption = document.createElement("option");
                defaultOption.value = "";
                defaultOption.text = "Seleccione un trabajador"
                select.appendChild(defaultOption);
                defaultOption.selected;
            }
            users.forEach(function(user){
                
                if(user.id !== responsible_id){
                    if(!Object.values(selectedUsersInputs).includes(user.id.toString())  || user.id === parseInt(currentValue)){
                        var option = document.createElement('option');
                        option.value = user.id;
                        option.textContent = user.name;
                        
                        option.selected = (user.id === parseInt(currentValue));
                        console.log("user_id: ", user.id, "vs curentValue: ", currentValue)
                        console.log(option.selected)
                        select.appendChild(option);
                    }   
                }
                
                
            })
            console.log("2 select value: ", select.value)

            if(!Object.values(selectedUsersInputs).includes("external") || currentValue === "external" ) {
                console.log("ingresa a externla if")
                var externalOption = document.createElement('option');
                externalOption.value = "external";
                externalOption.text = "Trabajador externo";
                select.appendChild(externalOption);
                externalOption.selected = (currentValue === "external");
                
            }
            
            if (select.value !== "external"){
                const parentDiv = select.parentElement;
                const inputElement = parentDiv.querySelector('input');
                if (inputElement) {
                    parentDiv.removeChild(inputElement);
                }
            }

        })
    }

}

