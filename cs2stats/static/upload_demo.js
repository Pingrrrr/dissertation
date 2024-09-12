document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', e => {
        if (e.lengthComputable) {
            processed = (e.loaded / e.total) * 100;
            document.getElementById('progress_bar').style.width = processed + '%';
        }
    });

    xhr.onload = function() {
        if (xhr.status === 200) {
            document.getElementById('status').innerText = 'Complete';
            //send a request to start parsing the demo file
        } else {
            document.getElementById('status').innerText = 'Error';
        }
    };

    xhr.open('POST', '');
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
    xhr.send(formData);
});