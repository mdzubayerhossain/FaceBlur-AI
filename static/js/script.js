// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const dropArea = document.getElementById('drop-area');
    const filePreviewContainer = document.getElementById('file-preview-container');
    const filePreview = document.getElementById('file-preview');
    const removeFileButton = document.getElementById('remove-file');
    const processButton = document.getElementById('process-button');
    const loader = document.querySelector('.loader');
    const results = document.getElementById('results');
    const resultMessage = document.querySelector('.result-message');
    const originalImage = document.getElementById('original-image');
    const processedImage = document.getElementById('processed-image');
    const downloadLink = document.getElementById('download-link');
    const tryAnotherButton = document.getElementById('try-another');
    const errorMessage = document.getElementById('error-message');

    // Handle drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.style.backgroundColor = 'rgba(107, 153, 214, 0.1)';
        dropArea.style.borderColor = 'var(--primary-color)';
    }

    function unhighlight() {
        dropArea.style.backgroundColor = '';
        dropArea.style.borderColor = '';
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) {
            fileInput.files = files;
            updateFilePreview();
        }
    }

    // Handle file selection
    fileInput.addEventListener('change', updateFilePreview);

    function updateFilePreview() {
        if (fileInput.files && fileInput.files[0]) {
            const file = fileInput.files[0];
            
            // Validate file type
            if (!file.type.match('image.*')) {
                showError('Please select an image file (JPEG, PNG, GIF).');
                resetForm();
                return;
            }

            // Show preview
            const reader = new FileReader();
            reader.onload = function(e) {
                filePreview.src = e.target.result;
                dropArea.classList.add('hidden');
                filePreviewContainer.classList.remove('hidden');
                processButton.disabled = false;
                hideError();
            };
            reader.readAsDataURL(file);
        }
    }

    // Remove selected file
    removeFileButton.addEventListener('click', resetForm);

    function resetForm() {
        fileInput.value = '';
        filePreview.src = '';
        dropArea.classList.remove('hidden');
        filePreviewContainer.classList.add('hidden');
        processButton.disabled = true;
    }

    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!fileInput.files || !fileInput.files[0]) {
            showError('Please select an image to process.');
            return;
        }

        // Show loader
        form.classList.add('hidden');
        loader.classList.remove('hidden');
        results.classList.add('hidden');
        hideError();

        // Create FormData
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        // Send request to server
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loader.classList.add('hidden');
            
            if (data.error) {
                showError(data.error);
                form.classList.remove('hidden');
                return;
            }

            // Show results
            resultMessage.textContent = data.message;
            originalImage.src = '/static/' + data.original_image;
            processedImage.src = '/static/' + data.processed_image;
            downloadLink.href = '/static/' + data.processed_image;
            results.classList.remove('hidden');
        })
        .catch(error => {
            loader.classList.add('hidden');
            form.classList.remove('hidden');
            showError('An error occurred during processing. Please try again.');
            console.error('Error:', error);
        });
    });

    // Try another image
    tryAnotherButton.addEventListener('click', function() {
        results.classList.add('hidden');
        resetForm();
        form.classList.remove('hidden');
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    }

    function hideError() {
        errorMessage.textContent = '';
        errorMessage.classList.add('hidden');
    }
});