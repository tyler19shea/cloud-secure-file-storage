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
                messageDiv.className = 'success';
            } else {
                messageDiv.textContent = 'File upload failed: ' + xhr.responseText;
                messageDiv.className = 'error';
            }
        };
        xhr.onerror = function () {
            var messageDiv = document.getElementById('message');
            messageDiv.textContent = 'Error during file upload';
            messageDiv.className = 'error';
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
                messageDiv.className = 'success';
            } else {
                var reader = new FileReader();
                reader.onload = function() {
                    var response = JSON.parse(reader.result);
                    messageDiv.textContent = 'File download failed: ' + response.message;
                    messageDiv.className = 'error';
                };
                reader.readAsText(xhr.response);
            }
        };
        xhr.onerror = function () {
            var messageDiv = document.getElementById('message');
            messageDiv.textContent = 'Error during file download';
            messageDiv.className = 'error';
        };
        xhr.send();
    });

    //Load file list
    function loadFiles() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/files', true);
        xhr.onload = function () {
            var messageDiv = document.getElementById('message');
            if (xhr.status === 200) {
                try {
                    var files = JSON.parse(xhr.responseText);
                    var fileListDiv = document.getElementById('file-list');
                    fileListDiv.innerHTML = '';
                    files.forEach(function(file) {
                        var fileDiv = document.createElement('div');
                        fileDiv.textContent = file;
                        fileListDiv.appendChild(fileDiv);
                    });
                } catch (e) {
                    messageDiv.textContent = 'Failed to parse file list response: ' + xhr.responseText;
                }
            } else {
                messageDiv.textContent = 'Failed to load file list: ' + xhr.responseText;
            }
        };
        xhr.onerror = function () {
            var messageDiv = document.getElementById('message');
            messageDiv.textContent = 'Error loading file list';
        };
        xhr.send();
    }

    // Load files on page load
    loadFiles();
});

