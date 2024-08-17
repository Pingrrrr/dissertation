document.addEventListener('DOMContentLoaded', function() {
    canvas = document.getElementById('map-canvas');
    ctx = canvas.getContext('2d');
    mapSelector = document.getElementById('map-selector');

    // load and display map
    function loadMap(mapName) {
        img = new Image();
        img.src = `/static/maps/${mapName}.png`; 
        img.onload = function() {
            // https://www.w3schools.com/tags/canvas_clearrect.asp & https://www.w3schools.com/jsref/canvas_drawimage.asp
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            
        };
        //https://www.w3schools.com/jsref/event_onerror.asp
        img.onerror = function() {
            console.error(`Could not load map: ${mapName}`);
        };
    }

   
    loadMap(mapSelector.value);
    mapSelector.addEventListener('change', function() {
        loadMap(this.value);
    });

    tools = document.querySelectorAll('.tool-icon');

    tools.forEach(tool => {
        tool.addEventListener('click', function() {
            // unselect all the tool items and then select only th clicked one
            tools.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
});