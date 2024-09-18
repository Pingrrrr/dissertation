//https://stackoverflow.com/a/40030387
var canvas = new fabric.Canvas('map-canvas', { preserveObjectStacking: true });
mapDropdown = document.querySelectorAll('.map-dropdown');

const saveButton = document.getElementById('saveButton');
editButtons = document.querySelectorAll('.edit-button');
currentColour = "black"

editButtons.forEach(button => {
    button.addEventListener('click', function (event) {

        event.preventDefault();

        if (this.textContent === "Edit") {

            a = this.parentElement.querySelector('.stratInput');
            a.removeAttribute("readonly");
            this.textContent = "Done";

        } else {

            a = this.parentElement.querySelector('.stratInput');
            a.setAttribute("readonly", "true");
            this.textContent = "Edit";

        }


    });
});

colourButtons = document.querySelectorAll('.colour-btn');

colourButtons.forEach(button => {
    button.addEventListener('click', function (event) {

        colour = this.querySelector('.dot').style.backgroundColor;
        document.getElementById('colour-indicator').style.backgroundColor = colour;
        currentColour = colour
        canvas.freeDrawingBrush.color = currentColour;

    });

})


var currentMap = "de_dust2"
var currentMapImg;
function setMap(oImg) {
    if (currentMapImg) {
        canvas.remove(currentMapImg);
    }
    oImg.set('selectable', false).set('erasable', false);
    oImg.scaleToHeight(800);
    oImg.scaleToWidth(800);
    canvas.setBackgroundImage(oImg, canvas.renderAll.bind(canvas));
    currentMapImg = oImg;
}

function loadMap(mapName) {

    fabric.Image.fromURL(`/static/maps/${mapName}.png`, function (oImg) {
        setMap(oImg)
    });
    currentMap = mapName;
}

mapDropdown.forEach(button => {
    button.addEventListener('click', function (event) {

        loadMap(this.value);

    })

});

function saveStrategyForm(event) {
    event.preventDefault();

    stratCanvas = JSON.stringify(canvas); //try/catch this in case any thing goes wrong

    data = new FormData(event.target);
    data.append('map', currentMap)
    data.append('stratCanvas', stratCanvas)


    console.log("attempting post of " + data.get('map'))
    fetch('', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        body: data,
        redirect: "follow"
    }).then(response => {
        console.log('POST request successful:', response);
        location.reload();
    })
        .catch(error => {
            console.error('Error:', error);
        });

}

form = document.getElementById('saveStratForm')
form.addEventListener('submit', saveStrategyForm)

const tools = document.querySelectorAll('.tool-icon');
canvas.freeDrawingBrush.width = 10;

tools.forEach(tool => {
    tool.addEventListener('click', function () {
        tools.forEach(t => t.classList.remove('active'));
        this.classList.add('active');

        switch (this.id) {
            case "draw":
                canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
                canvas.freeDrawingBrush.width = 10;
                canvas.freeDrawingBrush.color = currentColour;
                canvas.isDrawingMode = true;
                break;
            case "erase":
                canvas.freeDrawingBrush = new fabric.EraserBrush(canvas);
                canvas.freeDrawingBrush.width = 50;
                canvas.isDrawingMode = true;
                break;
            case "undo":
                canvas.freeDrawingBrush = new fabric.EraserBrush(canvas);
                canvas.freeDrawingBrush.width = 50;
                canvas.freeDrawingBrush.inverted = true;
                canvas.isDrawingMode = true;
                break;


            case "select":
                canvas.isDrawingMode = false;
                break;

            case "delete":
                canvas.isDrawingMode = false;

                objects = canvas.getActiveObjects();

                for (object of objects) {
                    canvas.remove(object);
                }

                break;

            case "player":
                var circle = new fabric.Circle({
                    radius: 10, fill: currentColour, left: 100, top: 100, //need to adjust the size of the circle to the scale of the map
                    erasable: false
                })
                canvas.isDrawingMode = false;
                canvas.add(circle)
                circle.bringToFront();
                break;

            case "smoke":
                canvas.isDrawingMode = false;
                var circle = new fabric.Circle({
                    radius: 20, fill: "gray", left: 100, top: 100, opacity: 0.7,
                    erasable: false
                })
                canvas.add(circle)
                circle.bringToFront();
                break;

            case "molotov":
                canvas.isDrawingMode = false;
                var circle = new fabric.Circle({
                    radius: 20, fill: "orange", left: 100, top: 100, opacity: 0.7,
                    erasable: false
                })
                canvas.add(circle)
                circle.bringToFront();
                break;
            case "grenade":
                canvas.isDrawingMode = false;
                var circle = new fabric.Circle({
                    radius: 15, fill: "red", left: 100, top: 100, opacity: 0.7,
                    erasable: false
                })
                canvas.add(circle)
                circle.bringToFront();
                break;
            case "flash":
                canvas.isDrawingMode = false;
                var circle = new fabric.Circle({
                    radius: 15, fill: "white", left: 100, top: 100, opacity: 0.4,
                    erasable: false
                })
                canvas.add(circle)
                circle.bringToFront();
                break;

            case "bomb":
                canvas.isDrawingMode = false;
                var rect = new fabric.Rect({
                    left: 100,
                    top: 100,
                    fill: 'red',
                    width: 25,
                    height: 20,
                    erasable: false
                })
                canvas.add(rect)
                rect.bringToFront();
                break;

        }
    });
});

var rect = new fabric.Rect({
    left: 100,
    top: 100,
    fill: 'red',
    width: 20,
    height: 20,
    erasable: false
})


loadStrategy(canvas,'./canvas', e=>{
    //canvas.setBackgroundImage(null);
    //canvas.setBackgroundColor('');
    //loadMap(canvas, map);
    canvas.renderAll.bind(canvas);
} );
