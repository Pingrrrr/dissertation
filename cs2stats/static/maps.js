document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('map-canvas');
    const ctx = canvas.getContext('2d');
    const mapSelector = document.getElementById('map-selector');
    let drawing = false;
    let erasing = false;

    function loadMap(mapName) {
        const img = new Image();
        img.src = `/static/maps/${mapName}.png`;
        img.onload = function() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
        img.onerror = function() {
            console.error(`Could not load map: ${mapName}`);
        };
    }

    loadMap(mapSelector.value);
    mapSelector.addEventListener('change', function() {
        loadMap(this.value);
    });

    canvas.addEventListener('mousedown', (event) => {
        drawing = true;
        if (erasing) {
            ctx.globalCompositeOperation = 'destination-out'; // Set erase mode
        } else {
            ctx.globalCompositeOperation = 'source-over'; // Set draw mode
        }
    });

    canvas.addEventListener('mouseup', () => {
        drawing = false;
        ctx.beginPath();
    });

    canvas.addEventListener('mousemove', function(event) {
        if (!drawing) return;
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        ctx.lineWidth = 5;
        ctx.lineCap = 'round';
        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);
    });

    const tools = document.querySelectorAll('.tool-icon');

    tools.forEach(tool => {
        tool.addEventListener('click', function() {
            tools.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            if (this.id === 'erase') {
                erasing = true;
            } else {
                erasing = false;
            }
        });
    });
});
