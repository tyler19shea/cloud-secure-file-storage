document.addEventListener('DOMContentLoaded', function() {
    // Handle file upload
    document.getElementById('upload-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission

        var fileInput = document.getElementById('file');
        var file = fileInput.files[0];
        var formData = new FormData();
        formData.append('file', file);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', this.action, true);
        xhr.onload = function () {
            var messageDiv = document.getElementById('message');
            if (xhr.status === 200) {
                messageDiv.textContent = 'File uploaded and encrypted successfully!';
            } else {
                messageDiv.textContent = 'File upload failed: ' + xhr.responseText;
            }
        };
        xhr.onerror = function () {
            var messageDiv = document.getElementById('message');
            messageDiv.textContent = 'Error during file upload';
        };
        xhr.send(formData);
    });

    // Handle file download
    document.getElementById('download-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission

        var filename = document.getElementById('filename').value;

        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/download/' + encodeURIComponent(filename), true);
        xhr.responseType = 'blob';
        xhr.onload = function () {
            var messageDiv = document.getElementById('message');
            if (xhr.status === 200) {
                var url = window.URL.createObjectURL(xhr.response);
                var a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                messageDiv.textContent = 'File downloaded successfully!';
            } else {
                messageDiv.textContent = 'File download failed: ' + xhr.responseText;
            }
        };
        xhr.onerror = function () {
            var messageDiv = document.getElementById('message');
            messageDiv.textContent = 'Error during file download';
        };
        xhr.send();
    });
});
