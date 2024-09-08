//https://stackoverflow.com/a/40030387
var canvas = new fabric.Canvas('map-canvas', { preserveObjectStacking:true });
const mapSelector = document.getElementById('map-selector');
let currentMap = ""
const saveButton = document.getElementById('saveButton');

var currentMapImg;
function setMap(oImg){
    if(currentMapImg){
        canvas.remove(currentMapImg);
    }    
    oImg.set('selectable',false).set('erasable', false);
    oImg.scaleToHeight(800);
    oImg.scaleToWidth(800);
    canvas.setBackgroundImage(oImg, canvas.renderAll.bind(canvas));
    currentMapImg = oImg;
}

function loadMap(mapName) {

    fabric.Image.fromURL(`/static/maps/${mapName}.png`, function(oImg) {
        setMap(oImg)
    });
    currentMap = mapName;
}

loadMap(mapSelector.value);
mapSelector.addEventListener('change', function() {
    loadMap(this.value);
});

function saveStrategyForm(event){
    event.preventDefault();

    stratCanvas = JSON.stringify(canvas); //try/catch this in case any thing goes wrong

    data = new FormData(event.target);
    data.append('map',currentMap)
    data.append('stratCanvas', stratCanvas)
    

    console.log("attempting post of "+ data.get('map'))
    fetch('',{
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
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
    tool.addEventListener('click', function() {
        tools.forEach(t => t.classList.remove('active'));
        this.classList.add('active');

        switch(this.id){
            case "draw":
                canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
                canvas.freeDrawingBrush.width = 10;
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

fetch('./canvas', {
    method: 'GET'
})
.then(response => {
    return response.json();
})
.then(json => {
    console.log(json)
    canvas.loadFromJSON(json);
})

canvas.add(rect)
rect.bringToFront();

