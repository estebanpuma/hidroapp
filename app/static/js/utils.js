function delete_thumbs(button) {
    const thumbnail = button.parentNode.parentNode;
    thumbnail.parentNode.removeChild(thumbnail)
    
};

function thumbs_process(){

    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('files');
    const imagePreview = document.getElementById('imagePreview');

    // Manejar la selección de archivos para previsualización
    //fileInput.addEventListener('change', function() {
        

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
